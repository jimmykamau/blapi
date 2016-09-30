import unittest
import flask_testing

from app import app


class TestAuthorization(flask_testing.TestCase):
    """
        Tests for authorization module
    """

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_user_registration(self):
        response = self.client.post('/auth/register')
        self.assertEqual(response.json, dict(success=True))

    def test_user_login(self):
        response = self.client.post('/auth/login')
        self.assertEqual(response.json, dict(success=True))


if __name__ == '__main__':
    unittest.main()
