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

**Q. Why do we add `-e .` at the end of `requirements.txt`?**

A. The `-e .` stands for **editable install**. It tells `pip` to install the local project (where `setup.py` exists) as a package in the current environment. 

- Instead of copying files to the `site-packages` directory, it creates a **symlink** to your project folder.
- This allows you to import your own local modules (e.g. `from cnnClassifier.config import ...`) from anywhere in the project, just like you would import an external library like `pandas` or `numpy`.
- Without `-e .`, you might get `ModuleNotFoundError` when trying to import from your own `src/cnnClassifier` folder.

---

**Q. Why do we create a Virtual Environment (`venv`) instead of installing globally?**

A. Virtual environments isolate your project's dependencies from your system's global Python and other projects. This ensures that:
- You don't get version conflicts between different projects (e.g. Project A needs standard Pandas, Project B needs older Pandas).
- It's easier to export an exact `requirements.txt` of only what *this* project uses.
- Your project is 100% reproducible on someone else's machine.

---

**Q. What is the difference between `setup.py` and `requirements.txt`?**

A. 
- **`requirements.txt`** lists *external* packages you need to download and install from PyPI (like pandas, tensorflow). It ensures the environment has the correct dependencies.
- **`setup.py`** is what packages *your own* project code. It makes your local directory (like `src/cnnClassifier`) installable. 
> *Interviewer Tip:* When we do `pip install -e .` (editable install), pip reads the `setup.py` file to know how to install your local code!

---

**Q. What is `setuptools.find_packages()` and why use it?**

A. In `setup.py`, `find_packages()` automatically scans your directory to find any folders containing an `__init__.py` file (like `components`, `config`, `utils`) and packages them. Without it, you would have to manually list out every single folder in your project whenever you add a new one.

**Q. Why do we initialize our custom `logger` inside `src/cnnClassifier/__init__.py`?**

A. The `__init__.py` file acts as the constructor / initializer for a Python package. 
- Any code inside it runs the exact moment the package is imported anywhere in the project.
- By placing our global `logger` setup there, we guarantee that the `logs/` directory is created and the logging configuration is defined **before** any other part of the project tries to use it.
- This allows us to simply do `from cnnClassifier import logger` cleanly in any file (like `main.py`).

---

**Q. Why do we wrap our read YAML/JSON files inside a `ConfigBox` in `common.py`?**

A. Normally, when you read a YAML or JSON file in Python, it returns a standard dictionary (`d = {"key": "value"}`). You are forced to access elements using brackets: `d["key"]`. If you try `d.key`, Python throws a nasty `AttributeError`.
By passing the dictionary into a `ConfigBox(d)`, we can access our variables cleanly using dot notation (`d.key`). It makes accessing config parameters throughout the entire pipeline extremely elegant and robust!

---

**Q. Why do we use `@ensure_annotations` decorators on our utility functions?**

A. Python is dynamically typed. Even if you define a function expecting a path string `def read_file(path: str)`, Python will happily let you pass an integer `read_file(5)` into it, causing a crash deep inside the logic. 
`@ensure_annotations` enforces strict type checking. It guarantees that if the function receives the wrong data type, it throws a precise `EnsureError` immediately, preventing silent bugs from propagating through models.

---

**Q. When initializing a GitHub repository with an empty `.github/workflows/main.yml` file, why does GitHub mark every commit with a red "Failure" X?**

A. GitHub Actions automatically scans the `.github/workflows/` directory on every push. It expects every YAML file inside to have at least two mandatory components:
1. `on:` (the trigger, e.g., on push to main)
2. `jobs:` (the code that tells a server what to run)
If the file is 100% empty, the GitHub parser immediately crashes trying to parse the empty required schema, failing the entire CI/CD pipeline. Adding a minimal "dummy" echo script satisfies the parser until real deployment code is written later.

---

**Q. Why does passing an empty `.yaml` file into `ConfigBox` completely crash the pipeline?**

A. When `yaml.safe_load()` attempts to read a completely blank file (0 bytes), it does not return an empty dictionary (`{}`). Instead, it returns Python's `None` primitive. When that `None` object is passed into `ConfigBox(None)`, the library throws a fatal `BoxValueError` because it demands a dictionary layout to create object dot-notation mappings. It is fixed by adding a dummy `key: value` pair so the YAML reads accurately as a dictionary block.

---

**Q. What causes `NameError: name 'XYZ' is not defined` inside a Jupyter Notebook when the class is clearly written earlier in the file?**

A. Jupyter Notebooks execute sequentially mapped to memory cell-by-cell. Even if the code is physically visible in the document above, if you forget to actually click "Run" (`Shift + Enter`) on the cell that defines the class/function, its variables are never injected into the active Python environment namespace. When a lower cell is run that calls it, Python throws a `NameError` because the reference doesn't exist in memory yet.

---

## 🤖 Prepare Base Model / Transfer Learning

**Q. What is Transfer Learning and why did we use it here instead of training from scratch?**

A. Transfer Learning reuses a model that was already trained on a large dataset (VGG16 was trained on 1.2 million ImageNet images). Instead of teaching a CNN to see from scratch — which would require massive compute time, data, and resources — we borrow the 14 learned convolutional layers that already know how to detect visual features (like edges, textures, shapes). We only train the final 2 classification layers on our small chicken fecal image dataset. This is dramatically faster, uses far less data, and achieves better accuracy than training from scratch.

---

**Q. What does `include_top=False` do in `tf.keras.applications.vgg16.VGG16()`?**

A. VGG16's "top" refers to its final 3 fully-connected (Dense) layers that were originally used to classify 1000 ImageNet categories. By passing `include_top=False`, we surgically remove these layers and only keep the 14 convolutional layers (the feature extractor). We then attach our own custom Dense (2 classes, Softmax) output layer on top.

---

**Q. Why do we freeze VGG16's layers during Transfer Learning?**

A. If we allowed training to update VGG16's pre-trained weights, the gradient updates from our tiny chicken dataset would quickly overwrite and destroy the powerful visual representations learned from 1.2 million ImageNet images. By setting `model.trainable = False`, we freeze those weights permanently. Only the 2 new Dense layers we added train from scratch — drastically reducing overfitting and training time.

---

## 🔔 Training Callbacks

**Q. What is a Keras Callback and why do we use them?**

A. Keras Callbacks are hook functions that automatically trigger at specific points during `model.fit()` — after each epoch, after each batch, etc. — without needing to write a manual training loop. They let you monitor training in real-time, save models automatically, and adjust hyperparameters on the fly, all because Keras calls them internally.

---

**Q. What is TensorBoard and how is it used in this project?**

A. TensorBoard is TensorFlow's real-time browser dashboard for visualizing training metrics like accuracy and loss curves during and after training. In this project, a new uniquely timestamped log directory (`tb_logs_at_YYYY-MM-DD-HH-MM-SS`) is created for each training run to prevent old runs from being overwritten. Once training starts, you visualize it live by running: `tensorboard --logdir ./artifacts/prepare_callbacks/tensorboard_log_dir`

---

**Q. Why do we use `save_best_only=True` in our ModelCheckpoint callback?**

A. Without `save_best_only=True`, Keras would overwrite the saved `.h5` model file after every epoch, even if the model's performance got worse. With `save_best_only=True`, the file is only overwritten when the validation accuracy improves upon the previous best — meaning the saved model always represents the peak performance across all training epochs.

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
