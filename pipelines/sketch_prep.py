import papermill as pm
from pathlib import Path
import sys
import os


def run_notebook_pipeline():
    """Run the sketch preparation pipeline (sketch generation + map generation)."""

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    notebooks_dir = project_root / "notebooks" / "sktech_creation"

    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return False

    os.chdir(notebooks_dir)
    print(f"Working directory: {os.getcwd()}")

    output_dir = Path("../../executed_notebooks")
    output_dir.mkdir(exist_ok=True)

    # Order: first generate sketches (if that notebook creates them), then generate maps
    pipeline_steps = [
        "sketch_gen.ipynb",  # assumed to create or collect sketches
        "sketch_postproc.ipynb",  # post-processes the generated sketches
    ]

    print("🚀 Starting Sketch Preparation Pipeline...")

    for i, notebook in enumerate(pipeline_steps, 1):
        input_path = Path(notebook)
        if not input_path.exists():
            print(f"❌ Missing notebook: {input_path}")
            return False
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

    print("\n🎉 Sketch preparation pipeline completed successfully!")
    return True


if __name__ == "__main__":
    success = run_notebook_pipeline()
    sys.exit(0 if success else 1)
