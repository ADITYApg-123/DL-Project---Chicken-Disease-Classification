# Step 3 — Environment Setup and Packages (`setup.py`)

📅 **Date:** 2026-03-22
🗂️ **Files worked on:** `setup.py`, VS Code Terminal

---

## 🔧 What I Did

### 1. Created `setup.py`
- Wrote the script that tells Python how to package our project (`cnnClassifier`).
- Filled out metadata such as version, author, GitHub repo URL, and description.

### 2. Configured `setuptools`
- Pointed the setup configuration to look for our source code inside the `src/` folder using `package_dir={"": "src"}`.
- Used `setuptools.find_packages()` so we never have to manually list out sub-folders like `components`, `pipeline`, etc.

### 3. Created and Activated a Virtual Environment
- Ran `python -m venv chicken` to create an isolated Python 3.12 environment.
- Ran `.\chicken\Scripts\activate` to enter the environment.

### 4. Installed Requirements
- Ran `pip install -r requirements.txt` to install all necessary Deep Learning libraries.
- The `-e .` at the end of `requirements.txt` automatically triggered our `setup.py` file, installing our local `src/cnnClassifier` as a Python package!

---

## 📄 Full Code in `setup.py`

```python
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "DL-Project---Chicken-Disease-Classification"
AUTHOR_USER_NAME = "ADITYApg-123"
SRC_REPO = "cnnClassifier"
AUTHOR_EMAIL = "aditya13pg@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for CNN app",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
```

---

## 💡 Key Concepts Learned

- **Virtual Environments (`venv`)** = Used to isolate dependencies so they don't corrupt the main system Python or other projects.
- **`setup.py` vs `requirements.txt`:** 
  - `requirements.txt` lists *external* tools to download.
  - `setup.py` is what packages *your own* local code.
- **`setuptools.find_packages()`** = Scans the directory and automatically packages any folder containing an `__init__.py` file.
