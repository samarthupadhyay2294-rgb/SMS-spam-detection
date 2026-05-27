import unittest
import os
import pickle
import numpy as np

from backend.utils.preprocess import clean_text, transform_text

class TestModelAssets(unittest.TestCase):
    def setUp(self):
        """Finds paths to serialized ML assets."""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(self.base_dir, 'backend', 'model', 'model.pkl')
        self.vectorizer_path = os.path.join(self.base_dir, 'backend', 'model', 'vectorizer.pkl')

    def test_assets_exist(self):
        """Verifies ML model binaries exist on disk in the correct folder."""
        self.assertTrue(os.path.exists(self.model_path), "model.pkl is missing from backend/model/")
        self.assertTrue(os.path.exists(self.vectorizer_path), "vectorizer.pkl is missing from backend/model/")

    def test_assets_loadable(self):
        """Verifies both pickle files load successfully and have the correct classes."""
        with open(self.vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        with open(self.model_path, 'rb') as f:
            model = pickle.load(f)
            
        self.assertIsNotNone(vectorizer, "Failed to deserialize vectorizer.")
        self.assertIsNotNone(model, "Failed to deserialize model.")
        
        # Check scikit-learn methods
        self.assertTrue(hasattr(vectorizer, 'transform'), "Vectorizer lacks transform method.")
        self.assertTrue(hasattr(model, 'predict'), "Model classifier lacks predict method.")
        self.assertTrue(hasattr(model, 'predict_proba'), "Model classifier lacks predict_proba method.")

    def test_prediction_pipeline(self):
        """Verifies prediction weights and shapes for sample messages."""
        with open(self.vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        with open(self.model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Benign test
        benign_text = "Are we still playing football tonight?"
        cleaned_text = clean_text(benign_text)
        transformed_text = transform_text(cleaned_text)
        
        vectorized = vectorizer.transform([transformed_text])
        prediction = model.predict(vectorized)[0]
        probabilities = model.predict_proba(vectorized)[0]
        
        self.assertEqual(len(probabilities), 2, "Binary probability list must have length 2.")
        self.assertAlmostEqual(sum(probabilities), 1.0, places=5, msg="Probabilities must sum to 1.0.")

if __name__ == '__main__':
    unittest.main()
