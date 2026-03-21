# Step 2 — Package Requirements (`requirements.txt`)

📅 **Date:** 2026-03-21
🗂️ **Files worked on:** `requirements.txt`

---

## 🔧 What I Did

### 1. Created `requirements.txt`
- Added all the necessary Python packages required for the Deep Learning Pipeline (TensorFlow, Pandas, Matplotlib, DVC, Flask, etc.)

### 2. Added `-e .` at the end
- Included `-e .` so that the local project (`src/cnnClassifier`) acts like an installed package.

---

## 📄 Full Code in `requirements.txt`

```text
tensorflow
pandas
dvc
notebook
numpy
matplotlib
seaborn
python-box==8.13.2
tqdm
ensure==1.0.0
joblib
types-PyYAML
scipy
Flask
Flask-Cors
scikit-learn
PyYAML
rich
-e .
```

---

## 💡 Key Concepts Learned

- **`requirements.txt`** = A file that lists all external dependencies your project needs to run. It makes sure that anyone running the project on another machine installs the exact same libraries.
- **`-e .` (Editable Install)** = This tells `pip` to install the local project folder (where `setup.py` lives) in "editable format". 
  - Instead of copying files, it creates a link to the original folder. 
  - This allows us to import our own folders like `from cnnClassifier.components import X`, just like we import external libraries!
  - It expects a `setup.py` file to exist in the same directory.
