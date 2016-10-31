import os
import json
import unittest
import flask_testing

from app import app, db
from blapi.bucketlists.tests.factories import \
    BucketlistFactory, BucketlistItemsFactory
from blapi.authorization.tests.factories import UserFactory


class TestAuthorization(flask_testing.TestCase):
    """
        Tests for bucketlists module
    """

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///test_bucketlist_models.sqlite"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        db.create_all()

    """@classmethod
                def tearDownClass(cls):
                    db.session.remove()
                    db.drop_all()
                    os.remove("test_bucketlist_models.sqlite")"""

    def login_user(self):
        factory_user = UserFactory.build()
        self.user_details = {
            'full_name': factory_user.full_name,
            'email': factory_user.email,
            'password': factory_user.password
        }
        response = self.client.post(
            '/auth/register', data=json.dumps(self.user_details),
            content_type='application/json')
        self.user_login_details = {
            'username': factory_user.email,
            'password': factory_user.password
        }
        response = self.client.post(
            '/auth/login', data=json.dumps(dict(self.user_login_details)),
            content_type='application/json')
        app.config['user_token'] = json.loads(
            response.data.decode('utf-8'))['access_token']
        app.config['auth_header'] = {
            'Authorization': 'JWT {}'.format(app.config['user_token'])
        }

    def test_bucketlist_creation(self):
        self.login_user()
        response = self.client.post(
            '/bucketlists/')
        self.assertEqual(response.json, dict(success=True))

    def test_list_all_bucketlists(self):
        response = self.client.get(
            '/bucketlists/', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_get_single_bucketlist(self):
        response = self.client.get(
            '/bucketlists/1', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_update_single_bucketlist(self):
        response = self.client.put(
            '/bucketlists/1', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_delete_single_bucketlist(self):
        response = self.client.delete(
            '/bucketlists/1', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_create_new_bucketlist_item(self):
        response = self.client.post(
            '/bucketlists/2/items/', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_update_bucketlist_item(self):
        response = self.client.put(
            '/bucketlists/2/items/1', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))

    def test_delete_bucketlist_item(self):
        response = self.client.delete(
            '/bucketlists/2/items/1', headers=app.config['auth_header'])
        self.assertEqual(response.json, dict(success=True))


if __name__ == '__main__':
    unittest.main()
