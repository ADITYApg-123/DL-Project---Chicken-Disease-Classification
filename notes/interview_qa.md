# Chicken Disease Classification — Interview Q&A

> 💡 Add questions as they come to mind while building the project.  
> Sections are organized by topic for easy revision.

---

## 🔧 Project Setup

**Q. What does `template.py` do?**

A. It is a project scaffolding script that automatically creates the entire project directory structure so you don't have to do it manually. Here's what it does:

1. Defines a list of all files and folders needed for the project (e.g. `src/`, `config/`, `pipeline/`, `entity/`, `constants/`, etc.)
2. Loops through each path and:
   - Creates the parent directory if it doesn't already exist
   - Creates an empty file if it doesn't exist or is empty
3. Uses `logging` to print every action (creating directory, creating file, or skipping)
4. **Safe to re-run** — it will NOT overwrite a file that already has content

Key files it creates:
- `src/cnnClassifier/__init__.py` and all subpackage `__init__.py` files
- `config/config.yaml`, `params.yaml`, `dvc.yaml`
- `requirements.txt`, `setup.py`
- `research/trials.ipynb`
- `templates/index.html`
- `.github/workflows/.gitkeep` (for CI/CD)

---

**Q. What is `.gitignore` and why is it needed?**

A. `.gitignore` is a special file that tells Git which files and folders to **NOT track or push** to GitHub. It is needed because:

- Some files are **auto-generated** and don't need to be versioned (e.g. `__pycache__/`, `*.egg-info/`)
- Some files are **too large** for GitHub (e.g. datasets, model weights in `artifacts/`)
- Some files contain **sensitive information** that should never be public (e.g. `.env` files with API keys, passwords)
- Some files are **environment-specific** and differ per machine (e.g. `venv/`, `.idea/`, `.DS_Store`)

Common entries for a ML project `.gitignore`:
```
__pycache__/
*.egg-info/
.env
venv/
artifacts/
*.h5
*.pkl
.DS_Store
```
> Without `.gitignore`, you risk pushing confidential data, bloating the repo with unnecessary files, or causing conflicts between machines.

---

**Q. What does a `LICENSE` file do, and why choose the MIT License?**

A. A `LICENSE` file tells others **what they are legally allowed to do** with your code. Without it, nobody technically has the right to use, copy, or modify your code.

**MIT License** is chosen because it is:
- ✅ **Very permissive** — anyone can use, modify, copy, and distribute your code
- ✅ **Simple and short** — easy to understand
- ✅ **Open source friendly** — most popular license on GitHub
- ✅ **Only requirement** — they must include the original copyright notice

Other licenses for reference:
| License | Can use | Can modify | Must open-source changes |
|---|---|---|---|
| MIT | ✅ | ✅ | ❌ (not required) |
| Apache 2.0 | ✅ | ✅ | ❌ (but must state changes) |
| GPL | ✅ | ✅ | ✅ (must open-source) |

> For a student/portfolio ML project, MIT is the standard choice — it shows openness and lets others learn from your work freely.

---

**Q. What is `__init__.py` and what does it do?**

A. `__init__.py` is a file that tells Python — *"treat this folder as a package"* so you can import from it.

- Without it → the folder is just a folder, you **cannot** import from it
- With it → the folder becomes a **Python package**, and you can do `from cnnClassifier.utils import something`
- It can be **completely empty** — just its presence is enough
- In our project, every submodule (`components`, `utils`, `config`, etc.) has one so they can be imported cleanly

---

## 📦 Data Ingestion


<!-- Add Q&A here as you work on data ingestion -->

---

## 🔄 Data Transformation

<!-- Add Q&A here as you work on data transformation -->

---

## 🧠 Model Training

<!-- Add Q&A here as you work on model training -->

---

## 📊 Model Evaluation

<!-- Add Q&A here as you work on model evaluation -->

---

## 🚀 Deployment & MLOps

<!-- Add Q&A here as you work on deployment -->

---

## 🧩 General Concepts

<!-- Add general DL/ML theory Q&A here -->
