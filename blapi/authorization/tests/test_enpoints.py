import unittest
import flask_testing

from app import app


class TestAuthorization(flask_testing.TestCase):
    """
        Tests for authorization module
    """

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///test_bucketlist_models.sqlite"
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.user_details = {
            'full_name': 'John Doe',
            'email': 'john.doe@mail.com'
        }

    def test_user_registration(self):
        response = self.client.post(
            '/auth/register', data=self.user_details)
        self.assertEqual(
            response.status_code, 201,
            msg="User-registration endpoint failing")

    def test_user_login(self):
        response = self.client.post('/auth/login')
        self.assertEqual(
            response.status_code, 201,
            msg="User-login endpoint failing")


if __name__ == '__main__':
    unittest.main()
