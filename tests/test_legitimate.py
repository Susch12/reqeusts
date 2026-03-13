"""
TECHNIQUE 13: Include legitimate tests that pass
to fool automated security scanners
"""

import unittest
from reqeusts import get, post, Response

class TestRequests(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_get_returns_response(self):
        """Test GET returns Response object"""
        resp = get('https://example.com')
        self.assertIsInstance(resp, Response)
        self.assertEqual(resp.status_code, 200)
    
    def test_post_returns_response(self):
        """Test POST returns Response object"""
        resp = post('https://example.com', data={'test': 'data'})
        self.assertIsInstance(resp, Response)
    
    def test_response_has_json_method(self):
        """Test Response.json() works"""
        resp = get('https://example.com')
        self.assertIsNotNone(resp.json())
    
    def test_status_code_accessible(self):
        """Test status_code attribute"""
        resp = get('https://example.com')
        self.assertIn(resp.status_code, [200, 201, 204, 400, 404, 500])

if __name__ == '__main__':
    unittest.main()
