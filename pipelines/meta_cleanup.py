import papermill as pm
from pathlib import Path
import sys
import os

def run_notebook_pipeline():
    """Run the amazing_logos_v4 processing pipeline"""
    
    # Change to the notebooks directory so notebook paths work correctly
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    notebooks_dir = project_root / "notebooks" / "amazing_logos_v4_cleanup"
    os.chdir(notebooks_dir)
    
    print(f"Working directory: {os.getcwd()}")
    
    # Now paths are relative to notebooks/amazing_logos_v4_cleanup folder
    output_dir = Path("../../executed_notebooks")
    output_dir.mkdir(exist_ok=True)
    
    # Define the pipeline order (with new shorter names)
    pipeline_steps = [
        #"step1.ipynb", # metadata extraction, outputs to metadata.csv
            # text splitting and cleaning (company, description, category, tags),
            # top 10 tags in category or description gets to NA
        #"step2.ipynb", # -> metadata2.csv
        "step3_categories.ipynb", # normalizing categories -> metadata3.csv
        "step3_tags.ipynb", # normalizing tags -> metadata5.csv
        #"step4_categories.ipynb", # only analyze categories, -> categories_analysis2.csv
        "step4_categories2.ipynb", # consolidate categories, -> categories_analysis3.csv, metadata6.csv
        "step4_categories3.ipynb", # assign tag to unclassified category -> metadata7.csv
        "step4_categories4_filtering.ipynb", # filter out categories with count < 4 -> metadata8.csv
            #  This notebook performs final category cleanup:
            # - Loads metadata8.csv
            # - Changes categories to 'unclassified' if they're not in the consolidation_map.keys()
            # - For frequent unclassified categories (>5 occurrences), adds the original category to tags
            # - Saves the result as metadata9.csv
        "step5_categories.ipynb",
            # Add step6 to compute coarse top-level category column from metadata9
        "step6_categories.ipynb",
    ]
    
    print("🚀 Starting Amazing Logos V4 Processing Pipeline...")
    
    for i, notebook in enumerate(pipeline_steps, 1):
        input_path = Path(notebook)  # Notebooks are in current directory now
        output_path = output_dir / f"executed_{notebook}"
        
        print(f"\n📋 Step {i}/{len(pipeline_steps)}: {notebook}")
        
        try:
            pm.execute_notebook(
                input_path=str(input_path),
                output_path=str(output_path),
                progress_bar=True
            )
            print(f"✅ {notebook} completed successfully")
            
        except Exception as e:
            print(f"❌ {notebook} failed with error: {e}")
            print("🛑 Pipeline stopped due to error")
            return False
    
    print("\n🎉 Pipeline completed successfully!")
    print("\n📊 Generated files:")
    output_data = Path("../../output/amazing_logos_v4/data/amazing_logos_v4_cleanup")  # Relative to notebooks/amazing_logos_v4_cleanup folder
    if output_data.exists():
        for file in output_data.glob("*.csv"):
            print(f"   - {file.name}")
    
    return True

if __name__ == "__main__":
    success = run_notebook_pipeline()
    sys.exit(0 if success else 1)