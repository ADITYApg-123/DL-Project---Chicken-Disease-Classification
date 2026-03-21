import os
from pathlib import Path
import logging 

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)

project_name = "cnnClassifier"

list_of_files = [
    ".github/workflows/main.yml",
    "src/cnnClassifier/__init__.py",
    "src/cnnClassifier/components/__init__.py",
    "src/cnnClassifier/utils/__init__.py",
    "src/cnnClassifier/config/__init__.py",
    "src/cnnClassifier/config/configuration.py",
    "src/cnnClassifier/pipeline/__init__.py",
    "src/cnnClassifier/entity/__init__.py",
    "src/cnnClassifier/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "dvc.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
    ".github/workflows/.gitkeep"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    
    else:
        logging.info(f"{filename} already exists")