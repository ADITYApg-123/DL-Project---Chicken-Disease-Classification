# Step 4 — Custom Logging Setup

📅 **Date:** 2026-03-22
🗂️ **Files worked on:** `src/cnnClassifier/__init__.py`, `main.py`, `.vscode/settings.json`

---

## 🔧 What I Did

### 1. Created a Custom Logger
- Inside `src/cnnClassifier/__init__.py`, I wrote a custom logging configuration. 
- This automatically creates a `logs/` folder and saves every log message into `running_logs.log` while also printing it to the terminal (`sys.stdout`).
- Exported the `logger` object so it can be imported anywhere in the project simply by doing `from cnnClassifier import logger`.

### 2. Fixed VS Code Import Resolution
- When I tried to `Ctrl + Click` on `logger` inside `main.py`, VS Code's Pylance extension couldn't find the `cnnClassifier` package.
- I created `.vscode/settings.json` and added `"python.analysis.extraPaths": ["./src"]`.
- This tells Pylance to treat the `src/` folder as a root directory for imports, fixing the syntax highlighting and Go-To-Definition (`Ctrl+Click`) instantly.

---

## 📄 Full Code in `__init__.py`

```python
import os
import sys
import logging

# Format of the log message: [Timestamp: Log Level: Module Name: Line Number Message]
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(lineno)d %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath), # Saves logs to the file
        logging.StreamHandler(sys.stdout)  # Prints logs to the terminal
    ]
)

logger = logging.getLogger("cnnClassifierLogger")
```

---

## 💡 Key Concepts Learned

- **`__init__.py` acts as the package initializer:** Any code you put in here runs the moment you import *anything* from the package. This is why we initialize our global logger here!
- **`logging.handlers`:** We used two handlers:
  - `FileHandler`: Writes the strings into the `.log` file on disk.
  - `StreamHandler(sys.stdout)`: Spits the strings out directly into the terminal while the code runs.
- **VS Code `extraPaths`:** Sometimes IDEs struggle with `src/` layout structures. Explicitly adding `src` to `python.analysis.extraPaths` in `.vscode/settings.json` manually forces the language server to index your local package.
