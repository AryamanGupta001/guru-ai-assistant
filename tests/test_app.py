# tests/test_app.py
import unittest
import os
# Conditional import for app, adjust path as necessary if ROOT_DIR is not in PYTHONPATH
try:
    from app import app # Assuming app.py is in the parent directory of 'tests'
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and other test variables."""
        app.testing = True
        self.client = app.test_client()
        # You might want to mock environment variables or services here
        # os.environ['GEMINI_API_KEY'] = 'test_key_for_app_tests'


    def tearDown(self):
        """Executed after each test."""
        pass

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GURU is healthy!', response.data)

    def test_index_page(self):
        """Test the index page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to GURU AI', response.data) # Check for a known string

    def test_chat_api_success(self):
        """Test the chat API endpoint with valid data."""
        response = self.client.post('/api/chat', json={'message': 'Hello GURU'})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('reply', json_data)
        # self.assertEqual(json_data['reply'], 'GURU echoes: Hello GURU') # If placeholder is active

    def test_chat_api_no_message(self):
        """Test the chat API endpoint with no message."""
        response = self.client.post('/api/chat', json={})
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'No message provided')

if __name__ == '__main__':
    unittest.main()
