# Data Preparation for "Curated Logo Dataset for Generative AI"

This repository contains all the scripts used for the data preparation of the [Minimalistic Logos (Image, Sketch, Prompt)](https://www.kaggle.com/datasets/paulhornig/minimalistic-logos-sketches-and-prompts) dataset on Kaggle. The original data is based on the [Amazing Logos v4](https://huggingface.co/datasets/iamkaikai/amazing_logos_v4) dataset from Hugging Face.

This work was originally part of a master's thesis titled "Konditionierte KI-Generierung minimalistischer Logos: Konzeption, Auswahl und Evaluation eines Modellprototyps".

## Project Structure

- **`/pipelines`**: Contains the main scripts for data preprocessing.
- **`/utils`**: Includes helper functions used by the pipelines, e.g., for image processing and text normalization.
- **`/input`**: Directory for the input data.
- **`/output`**: This is where the processed data and generated images are saved.
- **`/doc`**: Documentation of the individual steps of the process.

## Dependencies

The project was developed with Python 3.11. The main packages are:

- `pandas`
- `papermill`
- `opencv-python`
- `scikit-learn`
- `Pillow`
- `torch`
- `diffusers`
- `controlnet_aux`
- `google-generativeai`
