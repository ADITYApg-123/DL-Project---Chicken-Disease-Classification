# Step 1 — Project Setup and Template

📅 **Date:** 2026-03-21
🗂️ **Files worked on:** `template.py`

---

## 🔧 What I Did

### 1. Wrote `template.py` — a project scaffolding script
- Automatically creates all folders and files needed for the project
- Instead of manually creating every folder, this script does it all in one go

### 2. Set up Logging
- Used Python's built-in `logging` module to track what the script is doing in real time

### 3. Defined project name and list of all files to create
- Stored the project name in a variable
- Listed every file path the project needs in `list_of_files`

---

## 📄 Full Code Written in `template.py`

```python
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
```

---

## 🔍 What Each Part Does

### Imports
| Line | Purpose |
|---|---|
| `import os` | To create directories and check if files exist |
| `from pathlib import Path` | To handle file paths cleanly across OS (Windows/Linux/Mac) |
| `import logging` | To print log messages while the script runs |

### `logging.basicConfig()`
| Parameter | Purpose |
|---|---|
| `level=logging.INFO` | Show only INFO and above (skip DEBUG) |
| `format='[%(asctime)s]...'` | Format of each log line — timestamp, logger name, level, message |

> `%(asctime)s` uses old-style Python `%` formatting — prints the **actual timestamp**, not the word "asctime"

### `project_name = "cnnClassifier"`
- Stores the project name as a variable so it can be reused in all file paths
- Makes it easy to rename the project later — change it in just **one place**

### `list_of_files`
A Python list of **all file paths** the project needs. The script loops through this and creates each one.

| File/Folder | Purpose |
|---|---|
| `.github/workflows/main.yml` | GitHub Actions CI/CD pipeline config |
| `.github/workflows/.gitkeep` | Forces Git to track this empty folder |
| `src/cnnClassifier/__init__.py` | Makes `cnnClassifier` a Python package |
| `components/__init__.py` | Subpackage for data processing components |
| `utils/__init__.py` | Subpackage for utility/helper functions |
| `config/__init__.py` | Subpackage for configuration handling |
| `config/configuration.py` | Actual configuration logic — reads `config.yaml` and returns config objects |
| `pipeline/__init__.py` | Subpackage for training & prediction pipelines |
| `entity/__init__.py` | Subpackage for data classes / config entities |
| `constants/__init__.py` | Subpackage for project-wide constants |
| `config/config.yaml` | Main config file (paths, parameters) |
| `params.yaml` | Model hyperparameters |
| `dvc.yaml` | DVC pipeline stages definition |
| `requirements.txt` | List of Python packages to install |
| `setup.py` | Makes the project installable as a package |
| `research/trials.ipynb` | Jupyter notebook for experiments |
| `templates/index.html` | HTML template for the web app |

### The File Creation Loop
This loop runs through every path in `list_of_files` and creates the folders/files safely:

| Line / Function | Purpose |
|---|---|
| `Path(filepath)` | Converts string path to a Windows/Linux compatible Path object |
| `os.path.split()` | Splits `"folder/file.txt"` into `folder` and `file.txt` |
| `os.makedirs(..., exist_ok=True)` | Creates the folder. `exist_ok=True` means don't throw an error if it already exists |
| `os.path.exists(...)` | Checks if the file already exists |
| `os.path.getsize(...) == 0` | Checks if the file is completely empty |
| `with open(..., "w") as f: pass` | Creates an empty file (or overwrites it if empty) |

*(The logic safely creates files **only** if they don't exist or are empty, so you never accidentally overwrite actual code later!)*

---

## 💡 Key Concepts Learned

- **`template.py`** = scaffolding script — auto-creates the full project structure
- **`project_name` variable** = store once, reuse everywhere — easy to maintain
- **`list_of_files`** = central list of all files; script loops through to create each one
- **`__init__.py`** = makes a folder a Python **package** so it can be imported
- **`.gitkeep`** = dummy file to force Git to track an empty folder (Git ignores empty folders by default)
- **`logging.basicConfig()`** = configures how log messages look and which levels to show
- **`os.path.split()`** and **`os.makedirs()`** = essential OS tools for separating folders from file names and creating directories
