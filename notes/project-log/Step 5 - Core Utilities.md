# Step 5 — Core Utilities (`common.py`)

📅 **Date:** 2026-03-22
🗂️ **Files worked on:** `src/cnnClassifier/utils/common.py`

---

## 🔧 What I Did

Wrote a collection of highly reusable utility functions inside `common.py` that will be used throughout every stage of the MLOps pipeline (data ingestion, preprocessing, training, evaluation, and deployment).

Every single function uses two major safeguards:
1. **`@ensure_annotations`**: A decorator that enforces strict data typing (e.g., throwing an error if a function expects a `Path` variable but receives an `int`).
2. **`cnnClassifier.logger`**: Every action logs its success straight to our global `running_logs.log` file so we can trace what happens when we run the pipeline.

### 🧪 Experimentation in `research/trials.ipynb`
Before writing these utilities permanently into `common.py`, we explicitly tested the difference between standard dictionaries and `ConfigBox`, as well as standard Python functions versus `@ensure_annotations` inside the Jupyter Notebook `research/trials.ipynb`. This notebook safely served as our sandbox to prove exactly why these MLOps utilities prevent silent bugs.

---

## 🛠️ The 9 Functions I Built

| Function Name | What it does | Why it's useful |
|---|---|---|
| **`read_yaml()`** | Opens a `.yaml` file securely and wraps it in a `ConfigBox`. | Allows calling config arguments as `config.data` instead of `config['data']`. |
| **`create_directories()`** | Takes a list of paths and safely generates all folders using `os.makedirs()`. | Uses `exist_ok=True` to never crash if the folder is already there. |
| **`save_json()`** | Safely dumps Python dictionaries into a `.json` file (`indent=4`). | Formatting output cleanly. |
| **`load_json()`** | Reads a `.json` file and returns it as a dot-accessible `ConfigBox`. | Clean json parsing. |
| **`save_bin()`** | Uses `joblib` to save massive binary objects (like Machine Learning models). | Faster/more efficient than default `pickle` for model saving. |
| **`load_bin()`** | Uses `joblib` to load massive binary objects back into RAM. | Loading saved ML models later in the pipeline. |
| **`get_size()`** | Wraps `os.path.getsize` and returns file sizes natively in KB. | Great for logging dataset sizes or model sizes automatically. |
| **`encodeImageIntoBase64()`** | Reads an image and converts its binary matrix into a `base64` string. | Used in our Web App (Flask API) to pass images over the internet without files. |
| **`decodeImage()`** | Decodes a `base64` string back into a physical image file. | Used in our Web App when a user uploads an image payload. |

---

## 💡 Key Concepts Learned

- **`ConfigBox`**: A magical Python dictionary. Usually, if you have a dict (`d = {"key": "value"}`), you MUST access it using brackets `d["key"]`. By wrapping it in `ConfigBox(d)`, you can treat it like an object: `d.key`. Highly preferred for clean AI/ML codebase configurations!
- **`@ensure_annotations`**: Python is dynamically typed. Even if you annotate `def f(a: int):`, Python will happily accept `f("hello")`. By adding this decorator, we force Python to strictly validate types, preventing massive debugging headaches later in the AI pipeline.
