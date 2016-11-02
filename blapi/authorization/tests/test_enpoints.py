import flask_testing
import json
import unittest

from app import app, db
from blapi.authorization.tests.factories import UserFactory


class TestAuthorization(flask_testing.TestCase):
    """
        Tests for authorization module
    """

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///test_bucketlist_models.sqlite"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        db.create_all()
        db.session.expire_on_commit = False

    def test_user_registration(self):
        factory_user = UserFactory.create()
        self.user_details = {
            'full_name': factory_user.full_name,
            'email': factory_user.email,
            'password': factory_user.password
        }
        app.config['user_details'] = factory_user
        response = self.client.post(
            '/auth/register', data=json.dumps(self.user_details),
            content_type='application/json')
        self.assertEqual(
            response.status_code, 201,
            msg="User-registration endpoint failing")

    def test_user_registration_login(self):
        registered_user = app.config['user_details']
        self.user_login_details = {
            'username': registered_user.email,
            'password': registered_user.password
        }
        response = self.client.post(
            '/auth/login', data=json.dumps(dict(self.user_login_details)),
            content_type='application/json')
        self.assertEqual(
            response.status_code, 200,
            msg="User-login endpoint failing")
        self.assertTrue(
            response.json['access_token'],
            msg="Access token not being returned")

        # Check if private views require an access token
        auth_response = self.client.get(
            '/auth/register/1')
        self.assertTrue(
            auth_response.json['error'],
            msg="Private views being accessed without auth token")

        # Check if private views can be accessed with access token
        auth_response = self.client.get(
            '/auth/register/1',
            headers={
                'Authorization': 'JWT {}'.format(response.json['access_token'])
            }
        )
        self.assertEqual(
            auth_response.json['user'][0]['full_name'],
            registered_user.full_name)


if __name__ == '__main__':
    unittest.main()
