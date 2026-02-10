import papermill as pm
from pathlib import Path
import sys
import os


def run_notebook_pipeline():
    """Run the amazing_logos_v4 image preparation pipeline"""

    # Change to the notebooks directory so notebook paths work correctly
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    notebooks_dir = project_root / "notebooks" / "amazing_logos_v4_image_prep"
    os.chdir(notebooks_dir)

    print(f"Working directory: {os.getcwd()}")

    # Now paths are relative to notebooks/amazing_logos_v4_image_prep folder
    output_dir = Path("../../executed_notebooks")
    output_dir.mkdir(exist_ok=True)

    # Define the pipeline order
    # Assumed order based on typical data/image prep flow.
    # Adjust the order below if your workflow differs.
    pipeline_steps = [
        # 1. Extract images according to the prepared metadata
        "extract_images.ipynb",
        # 2. filtering step to exclude non-minimalistic logos
        "filter_minimalistic_logos.ipynb",
        # 3. Build the metadata used for image extraction
        "create_metadata10_from_total_filtered.ipynb",
        # 4. Create a class-balanced subset of images (if required for training/eval)
        "extract_balanced_images.ipynb",
        # Optional/experimental notebook, keep commented unless you want it in the pipeline
        # "test_ai_sketch_generation.ipynb",
    ]

    print("🚀 Starting Amazing Logos V4 Image Preparation Pipeline...")

    for i, notebook in enumerate(pipeline_steps, 1):
        input_path = Path(notebook)  # Notebooks are in current directory now
        output_path = output_dir / f"executed_{notebook}"

        print(f"\n📋 Step {i}/{len(pipeline_steps)}: {notebook}")

        try:
            pm.execute_notebook(
                input_path=str(input_path),
                output_path=str(output_path),
                progress_bar=True,
            )
            print(f"✅ {notebook} completed successfully")

        except Exception as e:
            print(f"❌ {notebook} failed with error: {e}")
            print("🛑 Pipeline stopped due to error")
            return False

    print("\n🎉 Pipeline completed successfully!")
    # If notebooks write artifacts to output/, they will already be in place.
    return True


if __name__ == "__main__":
    success = run_notebook_pipeline()
    sys.exit(0 if success else 1)
