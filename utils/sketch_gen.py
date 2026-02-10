"""Utility functions to call Google GenAI image-conditioned generation from notebooks.

This module intentionally does not execute code at import time. Use the `generate_from_*`
functions from a notebook such as `test_ai_sketch_generation_google`.

Example:
    from utils.sketch_gen import generate_from_path
    results = generate_from_path(
        prompt="Turn this sketch into a realistic 3D render in cyberpunk style.",
        image_path="sketch.png",
        api_key="YOUR_API_KEY",
        output_dir="./outputs",
    )

Returned value is a list of dicts with keys `image` (PIL.Image) and `path` (saved path or None).
"""

from typing import Optional, List, Dict, Union
import os
import base64
from io import BytesIO

try:
    from google import genai  # type: ignore
except Exception as e:  # pragma: no cover - only when dependency missing
    genai = None  # type: ignore

from PIL import Image


def _ensure_genai_available() -> None:
    if genai is None:
        raise ImportError(
            "google.genai is not available. Install the dependency and ensure it's importable."
        )


def get_client():
    """Return a genai.Client instance.

    Raises RuntimeError on failure with a helpful message.
    """
    _ensure_genai_available()
    try:
        return genai.Client()
    except Exception as exc:
        raise RuntimeError(f"Failed to create genai.Client: {exc}") from exc


def _make_image_part(image_bytes: bytes, mime_type: str = "image/png") -> dict:
    return {
        "inline_data": {
            "mime_type": mime_type,
            "data": base64.b64encode(image_bytes).decode("utf-8"),
        }
    }


DEFAULT_PROMPT = (
    "Take the provided logo image and redraw it as if it were a quick, abstract "
    "hand-drawn sketch.\n\n"
    "- Use the style of a pen or pencil on plain white paper.\n"
    "- Lines should look casual, uneven, and slightly imperfect, as if drawn quickly by hand.\n"
    "- Simplify details: keep only the basic shapes, contours, and key features of the logo.\n"
    "- Do not add shading, or effects — just minimal line work.\n"
    "- The sketch should feel like an informal draft or napkin sketch, not a polished digital rendering.\n\n"
    "The result should look like a handwritten sketch version of the logo, ready to be used "
    "as paired training data for sketch-to-logo generation."
)


def generate_from_bytes(
    image_bytes: bytes,
    prompt: Optional[str] = None,
    model: str = "gemini-2.5-flash-image-preview",
    save_outputs: bool = True,
    output_dir: str = ".",
    output_prefix: str = "output",
) -> List[Dict[str, Union[Image.Image, Optional[str]]]]:
    """Generate conditioned images from raw image bytes.

    Returns a list of dicts: {"image": PIL.Image, "path": <saved path or None>}.
    """
    _ensure_genai_available()
    client = get_client()

    final_prompt = prompt or DEFAULT_PROMPT
    image_part = _make_image_part(image_bytes)

    response = client.models.generate_content(model=model, contents=[final_prompt, image_part])

    results: List[Dict[str, Union[Image.Image, Optional[str]]]] = []

    if not hasattr(response, "candidates") or not response.candidates:
        return results

    content = response.candidates[0].content
    if not hasattr(content, "parts") or not content.parts:
        return results

    os.makedirs(output_dir, exist_ok=True)

    for i, part in enumerate(content.parts):
        if part.inline_data:
            img_data = part.inline_data.data
            img = Image.open(BytesIO(img_data)).convert("RGBA")

            saved_path: Optional[str] = None
            if save_outputs:
                fname = f"{output_prefix}_{i}.png"
                saved_path = os.path.join(output_dir, fname)
                img.save(saved_path)

            results.append({"image": img, "path": saved_path})

    return results


def generate_from_path(
    image_path: str,
    prompt: Optional[str] = None,
    model: str = "gemini-2.5-flash-image-preview",
    save_outputs: bool = True,
    output_dir: str = ".",
    output_prefix: str = "output",
) -> List[Dict[str, Union[Image.Image, Optional[str]]]]:
    """Read file at `image_path` and call `generate_from_bytes`.

    image_path may be a `str` or `pathlib.Path`.
    """
    with open(image_path, "rb") as f:
        data = f.read()
    return generate_from_bytes(
        image_bytes=data,
        prompt=prompt,
        model=model,
        save_outputs=save_outputs,
        output_dir=output_dir,
        output_prefix=output_prefix,
    )


if __name__ == "__main__":
    # Minimal CLI for quick manual tests. Not used by notebooks.
    import argparse

    parser = argparse.ArgumentParser(description="Call GenAI image-conditioned generation")
    parser.add_argument("image_path", help="Path to input image")
    parser.add_argument("--out", dest="output_dir", default=".")
    args = parser.parse_args()

    # Use default prompt unless one is supplied via env or additional CLI wiring
    res = generate_from_path(args.image_path, output_dir=args.output_dir)
    for r in res:
        print("saved:", r.get("path"))

