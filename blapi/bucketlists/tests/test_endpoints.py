import os
import json
import unittest
import flask_testing

from app import app, db
from blapi.bucketlists.tests.factories import \
    BucketlistFactory, BucketlistItemsFactory
from blapi.authorization.models import User
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
        db.session.expire_on_commit = False

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove("test_bucketlist_models.sqlite")

    def login_user(self):
        self.factory_user = UserFactory()
        self.user_details = {
            'full_name': self.factory_user.full_name,
            'email': self.factory_user.email,
            'password': self.factory_user.password
        }
        response = self.client.post(
            '/auth/register', data=json.dumps(self.user_details),
            content_type='application/json')
        self.user_login_details = {
            'username': self.factory_user.email,
            'password': self.factory_user.password
        }
        response = self.client.post(
            '/auth/login', data=json.dumps(dict(self.user_login_details)),
            content_type='application/json')
        user_token = json.loads(
            response.data.decode('utf-8'))['access_token']
        self.auth_header = {
            'Authorization': 'JWT {}'.format(user_token)
        }
        app.config['factory_user'] = self.factory_user
        app.config['auth_header'] = self.auth_header
        app.config['bucketlists'] = []

    def test_bucketlist_creation(self):
        self.login_user()
        self.factory_user_db = User.query.filter_by(
            full_name=self.factory_user.full_name).one()
        created_bucketlist = BucketlistFactory()
        self.bucketlist_details = {
            'name': created_bucketlist.name,
            'date_created': created_bucketlist.date_created.isoformat(),
            'date_modified': created_bucketlist.date_modified.isoformat(),
            'created_by': self.factory_user_db.id
        }
        app.config['bucketlists'].append(created_bucketlist)
        response = self.client.post(
            '/bucketlists/', data=json.dumps(dict(self.bucketlist_details)),
            headers=self.auth_header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_list_all_bucketlists(self):
        self.factory_user_db = User.query.filter_by(
            full_name=app.config['factory_user'].full_name).one()
        created_bucketlist = BucketlistFactory()
        self.bucketlist_details = {
            'name': created_bucketlist.name,
            'date_created': created_bucketlist.date_created.isoformat(),
            'date_modified': created_bucketlist.date_modified.isoformat(),
            'created_by': self.factory_user_db.id
        }
        app.config['bucketlists'].append(created_bucketlist)
        response = self.client.post(
            '/bucketlists/', data=json.dumps(dict(self.bucketlist_details)),
            headers=app.config['auth_header'], content_type='application/json')
        response = self.client.get(
            '/bucketlists/', headers=app.config['auth_header'])
        self.assertEqual(
            response.json['bucketlists'][0][0]['name'],
            app.config['bucketlists'][0].name
        )
        self.assertEqual(
            len(response.json['bucketlists'][0]),
            2
        )

    def test_get_single_bucketlist(self):
        response = self.client.get(
            '/bucketlists/1', headers=app.config['auth_header'])
        self.assertEqual(
            response.json['bucketlists'][0][0]['name'],
            app.config['bucketlists'][0].name
        )
        self.assertEqual(
            len(response.json['bucketlists'][0]),
            1
        )

    def test_update_single_bucketlist(self):
        self.updated_bucketlist_details = {
            'name': '{} new name'.format(app.config['bucketlists'][0].name)
        }
        response = self.client.put(
            '/bucketlists/1',
            data=json.dumps(dict(self.updated_bucketlist_details)),
            headers=app.config['auth_header'], content_type='application/json')
        self.assertEqual(
            response.json['bucketlist'][0]['name'],
            self.updated_bucketlist_details['name'])

    def test_create_new_bucketlist_item(self):
        created_bucketlist_item = BucketlistItemsFactory()
        self.bucketlist_item_details = {
            'name': created_bucketlist_item.name,
            'date_created': created_bucketlist_item.date_created.isoformat(),
            'date_modified': created_bucketlist_item.date_modified.isoformat(),
            'done': created_bucketlist_item.done,
            'bucketlist_id': 2
        }
        response = self.client.post(
            '/bucketlists/1/items/', headers=app.config['auth_header'],
            data=json.dumps(dict(self.bucketlist_item_details)),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist_item(self):
        self.updated_bucketlist_item_details = {
            'name': 'My new bucketlist item name',
            'done': True
        }
        response = self.client.put(
            '/bucketlists/1/items/1',
            data=json.dumps(dict(self.updated_bucketlist_item_details)),
            headers=app.config['auth_header'], content_type='application/json')
        self.assertEqual(
            response.json['bucketlist items'][0]['name'],
            self.updated_bucketlist_item_details['name'])

    def test_zdelete_bucketlist_item(self):
        response = self.client.delete(
            '/bucketlists/1/items/1', headers=app.config['auth_header'])
        response_2 = self.client.get(
            '/bucketlists/1/items/', headers=app.config['auth_header'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_2.json['bucketlist items'][0]), 0)

    def test_zdelete_single_bucketlist(self):
        response = self.client.delete(
            '/bucketlists/1', headers=app.config['auth_header'])
        response_2 = self.client.get(
            '/bucketlists/', headers=app.config['auth_header'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_2.json['bucketlists'][0]), 1)


if __name__ == '__main__':
    unittest.main()
