import os
import pickle
import numpy as np

from backend.utils.preprocess import clean_text, transform_text
from backend.utils.keyword_detector import detect_keywords
from backend.utils.confidence_score import calculate_confidence, determine_risk_level

# Paths to serialized assets
MODEL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(MODEL_DIR, 'model', 'model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'model', 'vectorizer.pkl')

# Global cache for loaded model and vectorizer
_model = None
_vectorizer = None

def load_assets():
    """
    Lazily loads the ML model and TF-IDF vectorizer binaries from disk.
    Caches the loaded models globally for sub-millisecond future predictions.
    """
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Model binaries not found. Ensure model.pkl and vectorizer.pkl "
                f"exist inside '{os.path.join(MODEL_DIR, 'model')}'."
            )
            
        with open(VECTORIZER_PATH, 'rb') as f:
            _vectorizer = pickle.load(f)
            
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
            
    return _model, _vectorizer

def predict_message(message_text):
    """
    Main prediction pipeline.
    1. Validates input bounds.
    2. Runs whitespace/punctuation cleaning.
    3. Transforms text (tokenization, stemming).
    4. Vectorizes using the pre-trained TF-IDF vectorizer.
    5. Predicts class (Spam/Safe) and returns continuous class probabilities.
    6. Identifies threat keywords.
    7. Evaluates confidence score and risk profile level.
    """
    # 1. Validation
    if not isinstance(message_text, str) or not message_text.strip():
        return {
            "prediction": "Safe",
            "confidence": 0.0,
            "risk_level": "Low",
            "probability": 0.0,
            "keywords": []
        }
        
    if len(message_text) > 1000:
        message_text = message_text[:1000] # Cap length for safety
        
    # Load ML assets
    model, vectorizer = load_assets()
    
    # 2 & 3. Preprocess
    # Clean text (lowercasing, punctuation stripping)
    cleaned = clean_text(message_text)
    # Advanced transform (stemming, stopwords removal)
    transformed = transform_text(cleaned)
    
    # 4. Vectorize
    vectorized = vectorizer.transform([transformed])
    
    # 5. Predict
    prediction_raw = model.predict(vectorized)[0]
    probabilities_raw = model.predict_proba(vectorized)[0] # Class probabilities
    
    # Map predictions to labels
    # If standard label encoding: 0 = Safe/Ham, 1 = Spam
    if isinstance(prediction_raw, (int, np.integer)):
        prediction_label = "Spam" if prediction_raw == 1 else "Safe"
        spam_prob = float(probabilities_raw[1])
    else:
        # If it returned a string like 'spam' or 'ham'
        pred_str = str(prediction_raw).strip().lower()
        prediction_label = "Spam" if pred_str in ['spam', '1'] else "Safe"
        
        # Figure out probability of spam index dynamically based on model classes
        if hasattr(model, 'classes_'):
            classes = list(model.classes_)
            spam_idx = -1
            for idx, cls in enumerate(classes):
                if str(cls).strip().lower() in ['spam', '1']:
                    spam_idx = idx
                    break
            if spam_idx != -1:
                spam_prob = float(probabilities_raw[spam_idx])
            else:
                spam_prob = float(probabilities_raw[-1])
        else:
            spam_prob = float(probabilities_raw[1]) if len(probabilities_raw) > 1 else float(probabilities_raw[0])
            
    # 6. Keywords
    keywords = detect_keywords(message_text)
    
    # 7. Confidence & Risk Level
    confidence = calculate_confidence(list(probabilities_raw))
    risk_level = determine_risk_level(prediction_label, spam_prob)
    
    return {
        "prediction": prediction_label,
        "confidence": confidence,
        "risk_level": risk_level,
        "probability": round(spam_prob, 3),
        "keywords": keywords
    }
