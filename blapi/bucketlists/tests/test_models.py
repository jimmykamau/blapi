import os
import datetime
import flask_testing
import unittest

from app import app, db
from blapi.authorization.models import User
from blapi.bucketlists.models import Bucketlist, BucketlistItems


class TestBucketlistModels(flask_testing.TestCase):
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

        bucketlist = Bucketlist(
            name="First bucketlist",
            date_created=datetime.datetime.now(),
            date_modified=datetime.datetime.now(),
            created_by=user_details.id
        )
        db.session.add(bucketlist)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("test_bucketlist_models.sqlite")

    def test_create_bucketlist(self):
        self.assertEqual(
            "First bucketlist",
            db.session.query(Bucketlist).filter_by(
                name="First bucketlist").one().name,
            msg="Cannot create bucket-list"
        )

    def test_create_bucketlist_item(self):
        bucketlist_item = BucketlistItems(
            name="First Bucketlist Item",
            date_created=datetime.datetime.now(),
            date_modified=datetime.datetime.now(),
            done=False,
            bucketlist_id=db.session.query(Bucketlist).filter_by(
                name="First bucketlist").one().id
        )
        db.session.add(bucketlist_item)
        db.session.commit()

        self.assertEqual(
            "First Bucketlist Item",
            db.session.query(BucketlistItems).filter_by(
                name="First Bucketlist Item").one().name,
            msg="Cannot create bucket-list item"
        )


if __name__ == '__main__':
    unittest.main()
