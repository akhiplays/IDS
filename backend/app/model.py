# model.py
import joblib
import numpy as np
import os

# model path relative to this file when running from backend/app
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "model", "xgb_model.joblib")

class IDSModel:
    def __init__(self, path=None):
        p = path or _MODEL_PATH
        if not os.path.exists(p):
            raise FileNotFoundError(f"Model file not found at {p}. Run training script to create it.")
        self.model = joblib.load(p)
        # if you used label encoder, load it here
        le_path = p.replace('.joblib', '.le.joblib')
        try:
            self.le = joblib.load(le_path) if os.path.exists(le_path) else None
        except Exception:
            self.le = None

    def predict(self, feature_vector):
        # feature_vector: 1D array-like of numeric features
        X = np.array(feature_vector).reshape(1, -1)
        proba = None
        try:
            proba = self.model.predict_proba(X)[0]
        except Exception:
            # fallback: model may not implement predict_proba
            pred = self.model.predict(X)[0]
            pred_label = str(pred)
            return {"label": pred_label, "confidence": 0.0}
        pred = self.model.predict(X)[0]
        if self.le is not None:
            try:
                pred_label = self.le.inverse_transform([int(pred)])[0]
            except Exception:
                pred_label = str(pred)
        else:
            pred_label = str(pred)
        # return label + confidence
        return {"label": pred_label, "confidence": float(max(proba))}
