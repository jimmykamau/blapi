import os
import flask_testing
import unittest

from app import app, db
from blapi.authorization.models import User


class TestAuthorizationModels(flask_testing.TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///test_bucketlist_models.sqlite"
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

        user_details = User(
            full_name="John Doe",
            email="john.doe@email.com",
            password="mysecurepassword",
            active=True,
        )
        db.session.add(user_details)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("test_bucketlist_models.sqlite")

    def test_create_user(self):
        self.assertEqual(
            "john.doe@email.com",
            db.session.query(User).filter_by(
                email="john.doe@email.com").one().email,
            msg="Cannot create user"
        )


if __name__ == '__main__':
    unittest.main()
