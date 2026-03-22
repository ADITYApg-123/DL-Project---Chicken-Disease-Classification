# Step 6 — Data Ingestion Pipeline (Detailed Revision Guide)

📅 **Date:** 2026-03-23
🗂️ **Files worked on:** `config/config.yaml`, `params.yaml`, `01_Data_Ingestion.ipynb`

This document serves as an in-depth breakdown of how the **Data Ingestion** pipeline was constructed in our Jupyter Notebook sandbox (`01_Data_Ingestion.ipynb`) before moving it to modular code. We followed our strict 9-step MLOps workflow.

---

## 1. Update `config.yaml`
We started by defining the fundamental paths and URLs in `config.yaml`. By keeping these out of the Python code, we ensure our code remains entirely decoupled from data sources.

```yaml
artifacts_root: artifacts

data_ingestion:
  root_dir: artifacts/data_ingestion
  source_URL: https://github.com/entbappy/Branching-tutorial/raw/refs/heads/master/Chicken-fecal-images.zip
  local_data_file: artifacts/data_ingestion/data.zip
  unzip_dir: artifacts/data_ingestion
```

---

## 2. Update `params.yaml`
We initialized `params.yaml` with a dummy key (`key: value`). This was a critical debugging step because an empty 0-byte YAML file returns Python's `None` primitive during `yaml.safe_load()`. This was crashing our custom `ConfigBox` utility, which requires a valid dictionary. 

---

## 3. Update the Entity
In MLOps, an **Entity** is just a custom data type (a `dataclass`) that rigidly defines what the return type of a configuration should look like.

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
```
*Why `frozen=True`?* It makes the dataclass immutable. Once the configuration is loaded, no one can accidentally overwrite `source_URL` somewhere else in the code.

---

## 4. Update the Configuration Manager
The `ConfigurationManager` is the brain that reads the YAML files and spits out the cleanly formatted Entities.

```python
class ConfigurationManager:
    def __init__(self, config_filepath=..., params_filepath=...):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root]) # Instantly builds 'artifacts/' folder

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir]) # Instantly builds 'artifacts/data_ingestion/'

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )
        return data_ingestion_config
```
Notice how extremely clean the dot-notation (`config.data_ingestion`) is? That's the power of the `ConfigBox` utility we wrote in `common.py`!

---

## 5. Update the Components
The Component is where the actual heavy lifting happens. For Data Ingestion, it means downloading the zip file over the internet and unzipping it into our freshly created local directories.

### A. Downloading the file
Using `urllib.request.urlretrieve`, we pull the massive `.zip` file from the cloud directly into `artifacts/data_ingestion/data.zip`. We also logged its exact filesize using our `get_size()` utility!

### B. Extracting the file
We used Python's built-in `zipfile` module:
```python
with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
    zip_ref.extractall(unzip_path)
```
This safely unpacks the entire dataset natively into `artifacts/data_ingestion/`.

---

## 6. Update the Pipeline (Final Execution)
Finally, we wrap everything in a clean `try-except` block to execute the notebook.

```python
try:
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
except Exception as e:
    raise e
```
**Why did we get a `NameError` earlier?** We tried to run this block before physically executing the Jupiter cells containing the classes above it. Python executes strictly in sequence mapped to memory, not just by what is visible on the screen!
