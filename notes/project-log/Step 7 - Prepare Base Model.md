# Step 7 — Prepare Base Model (VGG16 Transfer Learning)

📅 **Date:** 2026-04-06
🗂️ **Files worked on:**
- `config/config.yaml`
- `params.yaml`
- `src/cnnClassifier/entity/config_entity.py`
- `src/cnnClassifier/config/configuration.py`
- `src/cnnClassifier/components/prepare_base_model.py`
- `src/cnnClassifier/pipeline/stage_02_prepare_base_model.py`
- `main.py`

This document follows the strict 9-step MLOps pipeline workflow for the **Prepare Base Model** stage.

---

## 1. Update `config.yaml`
Added the base model configuration block pointing to where the downloaded and updated VGG16 models are stored:

```yaml
prepare_base_model:
  root_dir: artifacts/prepare_base_model
  base_model_path: artifacts/prepare_base_model/base_model.h5
  updated_base_model_path: artifacts/prepare_base_model/base_model_updated.h5
```

---

## 2. Update `params.yaml`
Added the key deep learning hyperparameters used to configure VGG16:

```yaml
IMAGE_SIZE: [224, 224, 3]       # Width, Height, RGB channels (VGG16 input requirement)
BATCH_SIZE: 16
INCLUDE_TOP: False               # removes the final classification layer (we add our own)
EPOCHS: 1
CLASSES: 2                       # Coccidiosis vs Healthy
WEIGHTS: imagenet                # Pre-trained on 1.2M ImageNet images
LEARNING_RATE: 0.01
```

---

## 3. Update the Entity
```python
@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int
```

---

## 4. Update the Configuration Manager
Added `get_prepare_base_model_config()` inside the existing `ConfigurationManager`. It reads from both
`config.yaml` (file paths) and `params.yaml` (hyperparameters), and natively creates the `artifacts/prepare_base_model/` directory.

---

## 5. Update the Component (`prepare_base_model.py`)
This is the most technically important file of this step. It has 3 key methods:

### `get_base_model()` — Load Vanilla VGG16
```python
self.model = tf.keras.applications.vgg16.VGG16(
    input_shape=self.config.params_image_size,   # [224, 224, 3]
    weights=self.config.params_weights,           # "imagenet"
    include_top=self.config.params_include_top    # False = remove the dense output layers
)
```
- **What is VGG16?** A 16-layer deep CNN by Oxford's Visual Geometry Group. Pre-trained on 1.2 million images (ImageNet dataset). Instead of training from scratch, we reuse all its learned visual feature maps (edges, textures, shapes).
- **Why `include_top=False`?** The "top" is VGG16's final Fully-Connected output layer, designed originally to classify 1000 object classes. Since we only need 2 classes (Coccidiosis vs Healthy), we remove it and add our own custom output layer.

### `_prepare_full_model()` — Freeze & Add Custom Head (Transfer Learning)
```python
# Freeze ALL layers (don't update existing VGG16 weights during training)
for layer in model.layers:
    model.trainable = False

# Add our own classification layers on top
flatten_in = tf.keras.layers.Flatten()(model.output)
prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(flatten_in)

full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)
full_model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"]
)
```
- **Why `freeze_all=True`?** VGG16's 14 Convolutional layers already know how to extract powerful features from images (edges → textures → shapes → objects). We don't need or want to destroy those 14-layer weights by retraining them on our tiny chicken dataset. We freeze them and only train the 2 new layers we added.
- **Why Flatten?** VGG16's final block outputs a 3D tensor (7x7x512). Dense classification layers need a 1D vector. `Flatten()` converts `(7, 7, 512)` → `(25088,)`.
- **Why Softmax?** For multi-class classification (2 classes here), Softmax converts raw logit scores into a probability distribution that sums to 1.0 (e.g., 92% Coccidiosis, 8% Healthy).

### `update_base_model()` — Save the Final Model
Saves both the raw base model and the updated (custom-headed) model as `.h5` files into our `artifacts` directory.

---

## 6. Update the Pipeline (`stage_02_prepare_base_model.py`)
```python
class PrepareBaseModelTrainingPipeline:
    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(prepare_base_model_config)
        prepare_base_model.get_base_model()      # Download & save vanilla VGG16
        prepare_base_model.update_base_model()   # Freeze + add custom head + save
```

---

## 7. Update `main.py`
`main.py` now orchestrates **two sequential pipeline stages**, each wrapped in its own `try-except` with fully logged separators:
```python
# Stage 1: Data Ingestion
obj = DataIngestionPipeline()
obj.main()

# Stage 2: Prepare Base Model (Transfer Learning)
obj = PrepareBaseModelTrainingPipeline()
obj.main()
```

---

## 💡 Key Concepts Learned

| Concept | Explanation |
|---|---|
| **Transfer Learning** | Reusing a model pre-trained on a large dataset (ImageNet) to solve a different task with far less data. The VGG16 feature extractor already knows the visual world; we just teach the final layer our specific classification. |
| **Freezing Layers** | Setting `model.trainable = False` prevents gradient updates from modifying the existing pre-trained weights during backpropagation. |
| **`include_top=False`** | Removes VGG16's final 3 Dense layers (1000-class output). We replace them with our own 2-class Softmax Dense layer. |
| **Categorical Cross-Entropy** | The standard loss function for multi-class classification tasks where each sample belongs to exactly one class. |
| **SGD Optimizer** | Stochastic Gradient Descent. Classic, reliable, and effective for fine-tuning Transfer Learning models. |
