# Step 8 — Prepare Callbacks (TensorBoard + ModelCheckpoint)

📅 **Date:** 2026-04-06
🗂️ **Files worked on:**
- `config/config.yaml`
- `src/cnnClassifier/entity/config_entity.py`
- `src/cnnClassifier/config/configuration.py`
- `src/cnnClassifier/components/prepare_callbacks.py`

This step follows our 9-step MLOps workflow to build the **training callbacks** that will monitor and checkpoint our model during the upcoming Training stage.

---

## 1. Update `config.yaml`
Added the `prepare_callbacks` configuration block:

```yaml
prepare_callbacks:
  root_dir: artifacts/prepare_callbacks
  tensorboard_root_log_dir: artifacts/prepare_callbacks/tensorboard_log_dir
  checkpoint_model_filepath: artifacts/prepare_callbacks/checkpoint_dir/model.h5
```

---

## 2. Update the Entity
```python
@dataclass(frozen=True)
class PrepareCallbacksConfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path
```

---

## 3. Update the Configuration Manager
Added `get_prepare_callback_config()` to the `ConfigurationManager`. 

One important detail here: `os.path.dirname()` is used to extract the parent directory of the checkpoint `.h5` filepath, since `create_directories()` needs a directory path not a file path. It then creates both the TensorBoard log directory and the checkpoint directory.

```python
def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
    config = self.config.prepare_callbacks
    model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
    create_directories([
        Path(model_ckpt_dir),
        Path(config.tensorboard_root_log_dir)
    ])
    ...
```

---

## 4. Update the Component (`prepare_callbacks.py`)

This component builds two industry-standard Keras callbacks for model training:

### Callback 1 — TensorBoard (`_create_tb_callbacks`)
```python
@property
def _create_tb_callbacks(self):
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    tb_running_log_dir = os.path.join(
        self.config.tensorboard_root_log_dir,
        f"tb_logs_at_{timestamp}",
    )
    return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)
```
- **What is TensorBoard?** TensorFlow's official real-time training dashboard. It visualizes training accuracy, validation accuracy, loss curves, and more as graphs you can explore in a browser.
- **Why timestamp?** Each training run gets its own uniquely named subfolder (e.g., `tb_logs_at_2026-04-06-03-50-00`). Without timestamps, every run would overwrite the previous run's logs.
- **Why `@property`?** It means calling `self._create_tb_callbacks` (without brackets `()`) already executes the method and returns the callback. Makes the final `get_tb_ckpt_callbacks()` method cleaner.

### Callback 2 — ModelCheckpoint (`_create_ckpt_callbacks`)
```python
@property
def _create_ckpt_callbacks(self):
    return tf.keras.callbacks.ModelCheckpoint(
        filepath=self.config.checkpoint_model_filepath,
        save_best_only=True
    )
```
- **What is ModelCheckpoint?** After every epoch, Keras evaluates the current validation accuracy. `ModelCheckpoint` automatically saves the model weights to disk **only when the validation accuracy has improved**. If an epoch performs worse, it doesn't save — we always keep the best-ever model!
- **Why `save_best_only=True`?** Without this, every epoch overwrites the saved model even if it got worse. With this flag, we are guaranteed our saved `.h5` file always holds the peak performance.

### Final Aggregation Method
```python
def get_tb_ckpt_callbacks(self):
    return [
        self._create_tb_callbacks,
        self._create_ckpt_callbacks
    ]
```
Returns both callbacks in a list, which is exactly the format Keras's `model.fit(callbacks=[...])` expects in the upcoming Training stage.

---

## 💡 Key Concepts Learned

| Concept | Explanation |
|---|---|
| **Keras Callbacks** | Special hook functions that automatically run at specific points during `model.fit()` (after each epoch, batch, etc.) without you having to write manual training loops. |
| **TensorBoard** | Real-time browser-based visualization of training metrics. Runs with `tensorboard --logdir ./artifacts/prepare_callbacks/tensorboard_log_dir`. |
| **ModelCheckpoint** | Saves the model at its best validation performance. The ultimate safety net against overfitting across epochs. |
| **`@property` decorator** | Turns a method into an attribute. Called without `()`. Makes code cleaner when returning single objects. |
