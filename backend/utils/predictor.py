import os
import pickle
import numpy as np

from backend.utils.preprocess import clean_text, transform_text
from backend.utils.keyword_detector import detect_keywords
from backend.utils.confidence_score import calculate_confidence, determine_risk_level

# Resolve model directory relative to project root (works on Render, Railway, local)
# backend/utils/predictor.py -> go up 2 levels to reach project root
_THIS_FILE = os.path.abspath(__file__)               # .../backend/utils/predictor.py
_UTILS_DIR = os.path.dirname(_THIS_FILE)             # .../backend/utils/
_BACKEND_DIR = os.path.dirname(_UTILS_DIR)           # .../backend/
_PROJECT_ROOT = os.path.dirname(_BACKEND_DIR)        # .../  (project root)

MODEL_DIR = os.path.join(_BACKEND_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
DATASET_PATH = os.path.join(_PROJECT_ROOT, 'dataset', 'spam.csv')

# Global cache for loaded model and vectorizer
_model = None
_vectorizer = None


def load_assets():
    """
    Lazily loads the ML model and TF-IDF vectorizer binaries from disk.
    Caches the loaded models globally for sub-millisecond future predictions.
    If the loaded model is determined to be unfitted, triggers an automated
    fallback self-healing training routine on the fly.
    """
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Model binaries not found at '{MODEL_DIR}'. "
                f"Ensure model.pkl and vectorizer.pkl are committed to the repo."
            )

        with open(VECTORIZER_PATH, 'rb') as f:
            _vectorizer = pickle.load(f)

        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)

        # Verify model fit status. Automatically heal if unfitted
        try:
            from sklearn.utils.validation import check_is_fitted
            check_is_fitted(_model)
        except Exception:
            print("Detected unfitted model.pkl. Running auto-healing fallback...")
            try:
                import csv

                texts = []
                labels = []
                with open(DATASET_PATH, mode='r', encoding='latin-1') as f:
                    reader = csv.reader(f)
                    next(reader)  # skip header
                    for row in reader:
                        if not row or len(row) < 2:
                            continue
                        label = 1 if row[0].strip().lower() == 'spam' else 0
                        labels.append(label)
                        texts.append(row[1])

                preprocessed = [transform_text(t) for t in texts]
                X_features = _vectorizer.transform(preprocessed)
                _model.fit(X_features, labels)

                try:
                    with open(MODEL_PATH, 'wb') as f:
                        pickle.dump(_model, f)
                    print("Auto-healed model saved to disk.")
                except Exception as save_err:
                    print(f"Could not persist healed model (read-only fs): {save_err}")

            except Exception as heal_err:
                print(f"Failed to execute automated model healing: {heal_err}")

    return _model, _vectorizer


def predict_message(message_text):
    """
    Main prediction pipeline.
    """
    if not isinstance(message_text, str) or not message_text.strip():
        return {
            "prediction": "Safe",
            "confidence": 0.0,
            "risk_level": "Low",
            "probability": 0.0,
            "keywords": []
        }

    if len(message_text) > 1000:
        message_text = message_text[:1000]

    model, vectorizer = load_assets()

    cleaned = clean_text(message_text)
    transformed = transform_text(cleaned)
    vectorized = vectorizer.transform([transformed])

    prediction_raw = model.predict(vectorized)[0]
    probabilities_raw = model.predict_proba(vectorized)[0]

    if isinstance(prediction_raw, (int, np.integer)):
        prediction_label = "Spam" if prediction_raw == 1 else "Safe"
        spam_prob = float(probabilities_raw[1])
    else:
        pred_str = str(prediction_raw).strip().lower()
        prediction_label = "Spam" if pred_str in ['spam', '1'] else "Safe"

        if hasattr(model, 'classes_'):
            classes = list(model.classes_)
            spam_idx = -1
            for idx, cls in enumerate(classes):
                if str(cls).strip().lower() in ['spam', '1']:
                    spam_idx = idx
                    break
            spam_prob = float(probabilities_raw[spam_idx]) if spam_idx != -1 else float(probabilities_raw[-1])
        else:
            spam_prob = float(probabilities_raw[1]) if len(probabilities_raw) > 1 else float(probabilities_raw[0])

    keywords = detect_keywords(message_text)
    confidence = calculate_confidence(list(probabilities_raw))
    risk_level = determine_risk_level(prediction_label, spam_prob)

    return {
        "prediction": prediction_label,
        "confidence": confidence,
        "risk_level": risk_level,
        "probability": round(spam_prob, 3),
        "keywords": keywords
    }
