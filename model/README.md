# Model folder

This folder will contain trained model artifacts created by `backend/scripts/train_xgboost.py`:

- `xgb_model.joblib` - trained XGBoost model
- `xgb_model.le.joblib` - label encoder (optional)
- `xgb_scaler.joblib` - scaler used during preprocessing

Run the training script to populate these files (see `README.md`).
