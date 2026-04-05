# 🗺️ Project Roadmap — Chicken Disease Classification

This checklist tracks our end-to-end progress across the entire project lifecycle.

## 1. Project Setup and Template ✅
- [x] Write `template.py` scaffolding script
- [x] Verify directory structure creation
- [x] Create project documentation structure (`notes/` folder)

## 2. Package Requirements ✅
- [x] Create and verify `requirements.txt`
- [x] Write `setup.py`

## 3. Data Ingestion ✅
- [x] Define data ingestion configuration
- [x] Write data downloading logic
- [x] Write data extraction logic
- [x] Update entity, configuration manager, and pipeline for ingestion
- [x] Test the data ingestion component

## 4. Default Model Architecture Preparation ✅
- [x] Download/load VGG16 base model with `include_top=False`
- [x] Freeze all convolutional layers (Transfer Learning)
- [x] Add custom Flatten → Dense (Softmax) classification head
- [x] Save base and updated models to `artifacts/`

## 5. Model Training ⬜
- [ ] Define training configuration with MLflow tracking (optional)
- [ ] Write custom training loop / callbacks
- [ ] Train the model on the data
- [ ] Update entity, configuration manager, and pipeline for training

## 6. Model Evaluation ⬜
- [ ] Write evaluation script
- [ ] Save metrics (accuracy, loss)
- [ ] Update entity, configuration manager, and pipeline for evaluation

## 7. Deployment (Web App) ⬜
- [ ] Create Flask / FastAPI application (`app.py`)
- [ ] Write inference/prediction pipeline
- [ ] Design simple front-end (`templates/index.html`)
- [ ] Test locally

## 8. CI/CD Pipeline (Optional) ⬜
- [ ] Write GitHub Actions workflows (`main.yml`)
- [ ] Configure Docker containerization
- [ ] Deploy to cloud (AWS/Azure)
