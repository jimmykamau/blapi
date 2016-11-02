import os
import flask_testing
import unittest

from app import app, db
from blapi.authorization.models import User
from blapi.authorization.tests.factories import UserFactory


class TestAuthorizationModels(flask_testing.TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///test_bucketlist_models.sqlite"
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

        factory_user = UserFactory()
        user_details = User(
            full_name=factory_user.full_name,
            email=factory_user.email,
            password=factory_user.password,
            active=True,
        )
        app.config['db_user_details'] = factory_user
        db.session.add(user_details)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("test_bucketlist_models.sqlite")

    def test_create_user(self):
        registered_user = app.config['db_user_details']

        self.assertEqual(
            registered_user.email,
            db.session.query(User).filter_by(
                email=registered_user.email).one().email,
            msg="Cannot create user"
        )

    def test_update_user(self):
        current_user = User.query.filter_by(
            full_name=app.config['db_user_details'].full_name).one()
        current_user.full_name = "Updated Name"
        db.session.add(current_user)
        db.session.commit()

        self.assertEqual(
            "Updated Name",
            User.query.filter_by(
                email=app.config['db_user_details'].email).one().full_name
        )

    def test_delete_user(self):
        current_user = User.query.filter_by(
            full_name=app.config['db_user_details'].full_name).one()
        db.session.delete(current_user)
        db.session.commit()

        self.assertEqual(
            len(User.query.filter_by(
                email=app.config['db_user_details'].email).all()),
            0
        )


if __name__ == '__main__':
    unittest.main()
