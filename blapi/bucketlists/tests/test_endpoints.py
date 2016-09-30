import unittest
import flask_testing

from app import app


class TestAuthorization(flask_testing.TestCase):
    """
        Tests for bucketlists module
    """

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_bucketlist_creation(self):
        response = self.client.post('/bucketlists')
        self.assertEqual(response.json, dict(success=True))

    def test_list_all_bucketlists(self):
        response = self.client.get('/bucketlists')
        self.assertEqual(response.json, dict(success=True))

    def test_get_single_bucketlist(self):
        response = self.client.get('/bucketlists/1')
        self.assertEqual(response.json, dict(success=True))

    def test_update_single_bucketlist(self):
        response = self.client.put('/bucketlists/1')
        self.assertEqual(response.json, dict(success=True))

    def test_delete_single_bucketlist(self):
        response = self.client.delete('/bucketlists/1')
        self.assertEqual(response.json, dict(success=True))

    def test_create_new_bucketlist_item(self):
        response = self.client.post('/bucketlists/2/items')
        self.assertEqual(response.json, dict(success=True))

    def test_update_bucketlist_item(self):
        response = self.client.put('/bucketlists/2/items/1')
        self.assertEqual(response.json, dict(success=True))

    def test_delete_bucketlist_item(self):
        response = self.client.delete('/bucketlists/2/items/1')
        self.assertEqual(response.json, dict(success=True))


if __name__ == '__main__':
    unittest.main()
