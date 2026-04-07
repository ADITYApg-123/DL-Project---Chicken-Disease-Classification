# 🐔 Chicken Disease Classification Project

An end-to-end Deep Learning (MLOps) project to classify chicken diseases based on fecal images using Convolutional Neural Networks (CNNs).

This repository contains the complete pipeline: from data ingestion to model training, evaluation, and finally deployment as a web application.

---

## 🔄 MLOps Pipeline Workflow
For every single stage of this project (Data Ingestion, Transformation, Training, Evaluation), we strictly follow this 9-step workflow:
1. Update `config.yaml`
2. Update `secrets.yaml` [Optional]
3. Update `params.yaml`
4. Update the entity
5. Update the configuration manager in `src/config`
6. Update the components
7. Update the pipeline
8. Update `main.py`
9. Update `dvc.yaml`

---

## 🚀 Progress So Far

We are currently building this project step-by-step. Here is what has been implemented so far:

### ✅ Step 1: Project Scaffolding (`template.py`)
Instead of manually creating dozens of folders and files for the pipeline, we wrote a Python script (`template.py`) that uses the standard Python `os` and `pathlib` libraries to automatically generate the complete MLOps directory architecture. 
- It sets up standard `src/` modular packages (components, pipeline, config, entity).
- It creates standard configuration files (`config.yaml`, `params.yaml`, `dvc.yaml`).
- It uses built-in logging (`logging.basicConfig`) to track creation.

### ✅ Step 2: Environment and Package Packaging
We defined all critical Deep Learning and utility dependencies (TensorFlow, Pandas, Matplotlib, DVC, etc.) in `requirements.txt`.
- We wrote `setup.py` and utilized `setuptools.find_packages()` to make the local `src/cnnClassifier` directory installable as a Python package.
- We used `-e .` (editable install) to link the project locally, allowing us to import our own modules cleanly (e.g. `from cnnClassifier.components import X`).

### ✅ Step 3: Core Utility Scripts (`common.py`)
We built 9 highly-reusable utility helper functions inside `src/cnnClassifier/utils/common.py` that power the entire pipeline:
- **`read_yaml`, `load_json`, `save_json`, `save_bin`, `load_bin`**: robust file I/O operations wrapped with custom logging.
- **`ConfigBox` implementation**: ensures our yaml dictionaries can be natively accessed via dot notation (`config.filepath` instead of `config['filepath']`).
- **`@ensure_annotations` enforcement**: prevents hidden data type crashes across the MLOps pipeline.
- Base64 encoding/decoding specifically built for our final Flask Web App architecture.

### ✅ Step 4: Data Ingestion Pipeline
We constructed the automated data ingestion system:
- Populated `config.yaml` with the external AWS/GitHub dataset URLs.
- Created `ConfigurationManager` to automatically parse YAML files into Python structures using our custom utilities.
- Built the `DataIngestion` class to programmatically download and extract complex dataset `.zip` structures directly into our isolated `artifacts/` database module.

### ✅ Step 5: Prepare Base Model (Transfer Learning with VGG16)
We implemented Transfer Learning instead of training a CNN from scratch:
- Loaded **VGG16** (pre-trained on 1.2M ImageNet images) with `include_top=False` to remove its 1000-class output layer.
- **Froze all 14 convolutional layers** so their learned feature maps are preserved during fine-tuning.
- Added a custom **Flatten → Dense (Softmax, 2 classes)** classification head for our binary chicken disease task.
- Compiled with **SGD optimizer** and **Categorical Cross-Entropy** loss.
- Saved both the raw base model and the updated custom-headed model into `artifacts/prepare_base_model/`.

### ✅ Step 6: Prepare Training Callbacks
Built two production-grade training callbacks to monitor and checkpoint the model during training:
- **TensorBoard**: Automatically logs per-epoch training metrics to a timestamped directory for real-time visualization in the browser.
- **ModelCheckpoint (`save_best_only=True`)**: Saves the model weights to disk only when validation performance improves — our safety net against overfitting.

---

## 🛠️ How to Run the Project (Current State)

If you are just cloning this repository and want to pick up exactly where we are, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/ADITYApg-123/DL-Project---Chicken-Disease-Classification.git
cd DL-Project---Chicken-Disease-Classification
```

### 2. Run the Template Script
If you want to recreate the empty modular folder structure from scratch:
```bash
python template.py
```
*(Check your terminal—it will log every folder and file it creates without overwriting any existing code!)*

### 3. Create a Virtual Environment
It is highly recommended to isolate the project dependencies using a virtual environment. We are using standard Python `venv`:
```bash
python -m venv chicken
```

### 4. Activate the Environment
- **Windows:**
  ```bash
  .\chicken\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source chicken/bin/activate
  ```

### 5. Install Dependencies & Local Package
Install the required packages and the local editable package (`-e .`):
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```text
├── .github/workflows/       # GitHub Actions CI/CD pipeline
├── config/                  # Configuration YAML files
├── notes/                   # Dev diary, project roadmap, and interview Q&A
├── research/                # Jupyter Notebooks for trials and experiments
├── src/cnnClassifier/       # ALL source code for the pipeline
│   ├── components/          # Python files for ingestion, training, etc.
│   ├── config/              # Configuration manager 
│   ├── constants/           # Global constants
│   ├── entity/              # Custom Data classes
│   ├── pipeline/            # End-to-end pipeline execution scripts
│   └── utils/               # Common helper functions
├── templates/               # HTML files for Flask Web App
├── dvc.yaml                 # DVC Pipeline stages tracking
├── params.yaml              # Hyperparameters configuration
├── requirements.txt         # External PIP dependencies
├── setup.py                 # Package setup and metadata
└── template.py              # Auto-scaffolding script
```

---

## 📝 Learning Resources & Notes
We are maintaining comprehensive documentation as we build this in the `notes/` directory:
- **`project_roadmap.md`:** The master checklist.
- **`project-log/`:** Step-by-step dev diary detailing what we did on each file and why.
- **`interview_qa.md`:** A growing list of potential interview questions based on the exact tools/concepts used.