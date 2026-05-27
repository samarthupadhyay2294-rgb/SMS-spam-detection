import unittest
import json
import os

# Set testing environment variables before importing the app factory
os.environ['FLASK_ENV'] = 'testing'
from backend.app import create_app

class TestSpamShieldAPI(unittest.TestCase):
    def setUp(self):
        """Initializes a Flask client and fresh isolated SQLite in-memory instance."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        """Verifies GET /health responds with 200 OK status."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'ok')

    def test_prediction_endpoint_valid_ham(self):
        """Verifies correct ham prediction outcomes."""
        payload = {"message": "Hey, do you want to grab lunch today?"}
        response = self.client.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('prediction'), 'Safe')
        self.assertEqual(data.get('risk_level'), 'Low')
        self.assertIn('confidence', data)
        self.assertIn('probability', data)
        self.assertIn('keywords', data)

    def test_prediction_endpoint_valid_spam(self):
        """Verifies correct spam threat classification."""
        payload = {"message": "FREE URGENT prize win lottery click now congratulations"}
        response = self.client.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('prediction'), 'Spam')
        self.assertIn(data.get('risk_level'), ['Medium', 'High'])
        self.assertGreater(data.get('confidence'), 50.0)
        # Check keywords matching
        self.assertTrue(len(data.get('keywords', [])) > 0)

    def test_prediction_endpoint_invalid_payload(self):
        """Verifies robust validation boundary rules."""
        # Test empty message
        response1 = self.client.post(
            '/predict',
            data=json.dumps({"message": "   "}),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 400)
        
        # Test missing field
        response2 = self.client.post(
            '/predict',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 400)

        # Test invalid type
        response3 = self.client.post(
            '/predict',
            data=json.dumps({"message": 12345}),
            content_type='application/json'
        )
        self.assertEqual(response3.status_code, 400)

        # Test too long text
        response4 = self.client.post(
            '/predict',
            data=json.dumps({"message": "x" * 1001}),
            content_type='application/json'
        )
        self.assertEqual(response4.status_code, 400)

    def test_api_history_sync(self):
        """Verifies database logging and syncing endpoints."""
        # Insert prediction
        payload = {"message": "Test history sync message lottery"}
        self.client.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Pull history
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]['message'], "Test history sync message lottery")

if __name__ == '__main__':
    unittest.main()
