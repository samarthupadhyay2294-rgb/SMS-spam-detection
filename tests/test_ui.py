import unittest
import os

os.environ['FLASK_ENV'] = 'testing'
from backend.app import create_app

class TestSpamShieldUI(unittest.TestCase):
    def setUp(self):
        """Initializes a Flask client for testing template renders."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_homepage_render(self):
        """Verifies index.html renders with all critical security hero tags."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        self.assertIn("SpamShield AI", html, "Homepage must render title logo.")
        self.assertIn("Interactive NLP Engine", html, "Homepage must render the scanner label.")
        self.assertIn("Platform Security Vectors", html, "Homepage must render the features label.")

    def test_aboutpage_render(self):
        """Verifies about.html technical documentation page renders successfully."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        self.assertIn("How It Works", html, "About page must render title.")
        self.assertIn("TF-IDF Vectorization", html, "About page must render TF-IDF documentation.")
        self.assertIn("Multinomial Naive Bayes", html, "About page must render MNB classification details.")

    def test_dashboard_render(self):
        """Verifies dashboard.html analytics interface renders successfully."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        self.assertIn("Security Analytics", html, "Dashboard page must render title.")
        self.assertIn("Threat Intelligence Console", html, "Dashboard page must render stats container.")
        self.assertIn("Live Threat Scan History", html, "Dashboard page must render table logs.")

if __name__ == '__main__':
    unittest.main()
