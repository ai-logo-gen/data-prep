import cv2
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import time
from pathlib import Path
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from controlnet_aux import CannyDetector
import torch
from controlnet_aux import LineartDetector
from controlnet_aux import HEDdetector
import os


def analyze_color_complexity(image_path, max_colors=10):
    """Analysiert die Farbkomplexität eines Logos"""
    img = cv2.imread(str(image_path))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape für Clustering
    pixels = img_rgb.reshape(-1, 3)
    
    # Eindeutige Farben zählen
    unique_pixels = np.unique(pixels, axis=0)
    unique_colors = len(unique_pixels)
    
    # K-Means für dominante Farben - aber nur wenn mehr als 1 eindeutige Farbe
    if unique_colors > 1:
        # Verwende die kleinere Zahl zwischen max_colors und tatsächlichen eindeutigen Farben
        n_clusters = min(max_colors, unique_colors)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Analysiere die Cluster-Zentren um wirklich dominante Farben zu finden
        labels = kmeans.labels_
        cluster_counts = np.bincount(labels)
        
        # Nur Cluster mit mindestens 1% der Pixel als "dominant" betrachten
        min_cluster_size = len(pixels) * 0.01
        dominant_colors = np.sum(cluster_counts >= min_cluster_size)
        
        # Falls alle Cluster zu klein sind, mindestens 1 dominante Farbe
        if dominant_colors == 0:
            dominant_colors = 1
    else:
        dominant_colors = 1
    
    return {
        'unique_colors': unique_colors,
        'dominant_colors': dominant_colors,
        'color_variance': np.var(pixels.astype(float))
    }

def analyze_edge_complexity(image_path):
    """Analysiert die Kantenkomplexität"""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    
    # Canny Edge Detection
    edges = cv2.Canny(img, 50, 150)
    edge_pixels = np.sum(edges > 0)
    total_pixels = img.shape[0] * img.shape[1]
    
    return {
        'edge_pixels': edge_pixels,
        'edge_ratio': edge_pixels / total_pixels,
        'edge_density': edge_pixels / (img.shape[0] * img.shape[1])
    }

def analyze_shape_complexity(image_path):
    """Analysiert die Formkomplexität"""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    
    # Threshold für Binärbild
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # Konturen finden
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Konturen analysieren
    num_contours = len(contours)
    total_contour_length = sum(cv2.arcLength(contour, True) for contour in contours)
    
    # Komplexität der größten Kontur
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        arc_length = cv2.arcLength(largest_contour, True)
        largest_contour_complexity = len(largest_contour) / arc_length if arc_length > 0 else 0
    else:
        largest_contour_complexity = 0
    
    return {
        'num_contours': num_contours,
        'total_contour_length': total_contour_length,
        'largest_contour_complexity': largest_contour_complexity
    }

def analyze_whitespace(image_path):
    """Analysiert den Weißraum-Anteil"""
    img = cv2.imread(str(image_path))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Weiße/helle Pixel zählen (Threshold bei 200)
    white_pixels = np.sum(img_gray > 200)
    total_pixels = img_gray.shape[0] * img_gray.shape[1]
    whitespace_ratio = white_pixels / total_pixels
    
    return {
        'whitespace_ratio': whitespace_ratio,
        'content_ratio': 1 - whitespace_ratio
    }


# Analyse-Funktion für pandarallel
def analyze_logo_row(row):
    """Analysiert ein Logo basierend auf DataFrame-Row"""
    try:
        logo_path = row['logo_path']
        
        # Alle Analysen durchführen
        color_analysis = analyze_color_complexity(logo_path)
        edge_analysis = analyze_edge_complexity(logo_path)
        shape_analysis = analyze_shape_complexity(logo_path)
        whitespace_analysis = analyze_whitespace(logo_path)
        
        # Ergebnis als Series zurückgeben
        result = pd.Series({
            **color_analysis,
            **edge_analysis,
            **shape_analysis,
            **whitespace_analysis
        })
        
        return result
        
    except Exception as e:
        print(f"Fehler bei {row['filename']}: {e}")
        # Fallback-Werte bei Fehler
        return pd.Series({
            'unique_colors': 0,
            'dominant_colors': 0,
            'color_variance': 0,
            'edge_pixels': 0,
            'edge_ratio': 0,
            'edge_density': 0,
            'num_contours': 0,
            'total_contour_length': 0,
            'largest_contour_complexity': 0,
            'whitespace_ratio': 0,
            'content_ratio': 0
        })
    

# Preprocessing function to avoid hand/finger artifacts
def preprocess_image_for_sketch(image, crop_bottom_percent=5):
    """
    Preprocess image to avoid hand/finger artifacts in generated sketches
    
    Args:
        image: PIL Image
        crop_bottom_percent: Percentage to crop from bottom to remove potential fingers
    """
    width, height = image.size
    
    # Option 1: Crop bottom portion where fingers usually appear
    crop_height = int(height * (100 - crop_bottom_percent) / 100)
    cropped_image = image.crop((0, 0, width, crop_height))
    
    # Resize back to original size with white padding at bottom
    final_image = Image.new('RGB', (width, height), color='white')
    final_image.paste(cropped_image, (0, 0))
    
    return final_image


# Sketch generation parameters
IMAGE_SIZE = (512, 512)  # ControlNet works best with 512x512
NUM_INFERENCE_STEPS = 25
GUIDANCE_SCALE = 8.0
CONTROLNET_SCALE = 0.8
# slow on gpu, but fast on cpu, created the nice looking sketches
def generate_sketch(image_path, pipeline_info, output_dir, use_preprocessing=True):
    """Generate a human-like sketch from an image using ControlNet"""
    
    if pipeline_info is None or pipeline_info[0] is None:
        print("❌ Pipeline not available")
        return None
    
    pipeline, model_type = pipeline_info
    print(f"🎨 Generating sketch for: {Path(image_path).name}")
    print(f"🔧 Using model: {model_type}")
    start_time = time.time()
    
    try:
        # Load and preprocess the image
        image = Image.open(image_path).convert("RGB")
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # Apply preprocessing to avoid finger artifacts
        if use_preprocessing:
            print("🧹 Preprocessing image to avoid finger artifacts...")
            image = preprocess_image_for_sketch(image, crop_bottom_percent=8)
        
        # Create control input based on model type
        print(f"🔍 Creating control input for {model_type}...")
        
        if model_type in ['lineart', 'lineart_anime']:
            # For lineart models, use simpler edge detection
            processor = LineartDetector.from_pretrained('lllyasviel/Annotators')
            control_image = processor(image)
        elif model_type == 'scribble':
            # For scribble, use HED edge detection
            processor = HEDdetector.from_pretrained('lllyasviel/Annotators')
            control_image = processor(image, scribble=True)
        else:  # canny
            canny_detector = CannyDetector()
            control_image = canny_detector(image, low_threshold=50, high_threshold=150)
        
        # Optimized prompts for simple line sketches
        positive_prompt = (
            "abstact sketch of a logo made by hand with simple drawed lines. The lines are curvy and not straight because it is drawn by hand."
            # "simple line drawing, minimal sketch, clean lines, "
            # "black lines on white background, line art, outline drawing, "
            # "simple sketch, minimalist drawing, basic outline, "
            # "thin black lines, white background"
        )
        
        negative_prompt = (
            ""
            "hands, fingers, human hand, thumb, palm, holding, gripping, pencil, exact match, shadows, straight lines, details"
            # "colored, filled areas, shading, shadows, gradients, "
            # "photographic, realistic, 3d render, complex details, "
            # "textured, painted, thick lines, multiple colors, "
            # "blurry, low quality, distorted, cartoon faces,"
            # "person, human body parts, skin, flesh"
        )
        
        print("🚀 Generating simple line sketch...")
        print(f"   Steps: {NUM_INFERENCE_STEPS}")
        print(f"   Guidance: {GUIDANCE_SCALE}")
        print(f"   ControlNet strength: {CONTROLNET_SCALE}")
        
        # Generate the sketch with optimized parameters for simple lines
        result = pipeline(
            prompt=positive_prompt,
            image=control_image,
            negative_prompt=negative_prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            controlnet_conditioning_scale=CONTROLNET_SCALE,
            guidance_scale=GUIDANCE_SCALE,
            generator=torch.Generator().manual_seed(42)  # For reproducible results
        )
        
        sketch = result.images[0]
        
        # Save the sketch
        output_filename = f"{Path(image_path).stem}_sketch_{model_type}.png"
        output_path = Path(output_dir) / output_filename
        sketch.save(output_path)
        
        generation_time = time.time() - start_time
        print(f"✅ Sketch generated in {generation_time:.1f} seconds")
        print(f"💾 Saved to: {output_path}")
        
        return {
            'original': image,
            'control': control_image,
            'sketch': sketch,
            'output_path': output_path,
            'generation_time': generation_time,
            'model_type': model_type
        }
        
    except Exception as e:
        print(f"❌ Error generating sketch: {e}")
        return None
    

MODEL_CACHE_DIR = '../../models/controlnet_cache'  # Local cache for models
# Centralized model id maps to keep selection consistent between setup functions
MODEL_MAP = {
    'lineart': 'lllyasviel/control_v11p_sd15_lineart',
    'lineart_anime': 'lllyasviel/control_v11p_sd15s2_lineart_anime',
    'canny': 'lllyasviel/control_v11p_sd15_canny',
}

FALLBACK_MODELS = {
    'lineart': 'lllyasviel/sd-controlnet-canny',
    'lineart_anime': 'lllyasviel/sd-controlnet-canny',
    'canny': 'lllyasviel/sd-controlnet-canny',
    'scribble': 'lllyasviel/sd-controlnet-canny'
}


def _load_controlnet_model(model_type: str):
    """Load a ControlNet model with fallback handling.

    Returns (controlnet, resolved_model_type, model_id_used)
    """
    if model_type not in MODEL_MAP and model_type not in FALLBACK_MODELS:
        print(f"❌ Unknown model type: {model_type}")
        return None, None, None, None

    model_id = MODEL_MAP.get(model_type, FALLBACK_MODELS.get(model_type))
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    print(f"🔄 Trying primary model: {model_id}")
    try:
        controlnet = ControlNetModel.from_pretrained(
            model_id,
            torch_dtype=dtype,
            cache_dir=MODEL_CACHE_DIR,
        )
        print(f"✅ Successfully loaded: {model_id}")
        return controlnet, model_type, model_id, dtype

    except Exception as e:
        # If there is a specified fallback for this logical model_type, try it
        fallback = FALLBACK_MODELS.get(model_type)
        if fallback is None:
            print(f"❌ ControlNet load failed and no fallback available: {e}")
            return None, None, None, None

        print(f"⚠️ Primary model failed: {e}")
        print(f"🔄 Trying fallback model: {fallback}")
        try:
            controlnet = ControlNetModel.from_pretrained(
                fallback,
                torch_dtype=dtype,
                cache_dir=MODEL_CACHE_DIR,
            )
            print(f"✅ Successfully loaded fallback: {fallback}")
            # reflect that we ended up using a canny-type controlnet
            return controlnet, 'canny', fallback, dtype

        except Exception as e2:
            print(f"❌ Both primary and fallback models failed:")
            print(f"   Primary error: {e}")
            print(f"   Fallback error: {e2}")
            return None, None, None, None

# Setup ControlNet pipeline for sketch generation
def setup_sketch_pipeline(model_type="lineart"):
    """Initialize the ControlNet pipeline for generating sketches
    
    model_type options:
    - 'lineart': Better for simple line drawings
    - 'lineart_anime': Anime-style line art
    - 'canny': Edge-based (current approach)
    - 'scribble': Hand-drawn scribble style
    """
    print(f"🔄 Loading ControlNet model: {model_type}")
    start_time = time.time()
    
    # Centralized model loading
    controlnet, resolved_type, used_model_id, dtype = _load_controlnet_model(model_type)
    if controlnet is None:
        return None, None
    model_type = resolved_type
    
    # Load Stable Diffusion pipeline with ControlNet (moved outside except block)
    try:
        try:
            pipe = _load_pipe(True, controlnet, dtype)
        except TypeError:
            pipe = _load_pipe(False, controlnet, dtype)
        
        pipe = _configure_pipe(pipe)
        
        load_time = time.time() - start_time
        print(f"✅ Pipeline setup complete in {load_time:.1f} seconds")
        
        return pipe, model_type
        
    except Exception as e:
        print(f"❌ Error setting up pipeline: {e}")
        return None, None


def _configure_pipe(pipe):
    """Common pipe configuration: scheduler, device placement, and optional accelerations."""
    # Use faster scheduler
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

    # Move to GPU if available
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
        print("🚀 Pipeline loaded on GPU")
    else:
        print("💻 Pipeline loaded on CPU")

    # Optional accelerations (xFormers disabled by default)
    try:
        # if 'USE_XFORMERS' in globals() and USE_XFORMERS:
        #     pipe.enable_xformers_memory_efficient_attention()
        #     print("⚡ XFormers acceleration enabled")
        # else:
        print("ℹ️ XFormers disabled (USE_XFORMERS=False)")
    except Exception as ex:
        print(f"ℹ️ XFormers not enabled: {ex}")

    try:
        pipe.enable_attention_slicing()
    except Exception:
        pass

    return pipe


def _load_pipe(with_safety_args: bool, controlnet, dtype=None):
    """Load StableDiffusionControlNetPipeline with consistent dtype and cache settings."""
    if dtype is None:
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    common_kwargs = dict(
        controlnet=controlnet,
        torch_dtype=dtype,
        cache_dir=MODEL_CACHE_DIR,
    )

    if with_safety_args:
        return StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            safety_checker=None,
            requires_safety_checker=False,
            **common_kwargs,
        )
    else:
        return StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            **common_kwargs,
        )