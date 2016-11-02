import os
import datetime
import flask_testing
import unittest

from app import app, db
from blapi.authorization.models import User
from blapi.authorization.tests.factories import UserFactory
from blapi.bucketlists.models import Bucketlist, BucketlistItems
from blapi.bucketlists.tests.factories import \
    BucketlistFactory, BucketlistItemsFactory


class TestBucketlistModels(flask_testing.TestCase):
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

        factory_user_db = User.query.filter_by(
            full_name=factory_user.full_name).one()
        created_bucketlist = BucketlistFactory()
        bucketlist = Bucketlist(
            name=created_bucketlist.name,
            date_created=created_bucketlist.date_created,
            date_modified=created_bucketlist.date_modified,
            created_by=factory_user_db.id
        )
        app.config['created_bucketlist'] = created_bucketlist
        db.session.add(bucketlist)
        db.session.commit()

        factory_bucketlist_item = BucketlistItemsFactory()
        bucketlist_item = BucketlistItems(
            name=factory_bucketlist_item.name,
            date_created=factory_bucketlist_item.date_created,
            date_modified=factory_bucketlist_item.date_modified,
            done=factory_bucketlist_item.done,
            bucketlist_id=Bucketlist.query.filter_by(
                name=app.config['created_bucketlist'].name).one().id
        )
        app.config['bucketlist_item'] = factory_bucketlist_item
        db.session.add(bucketlist_item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("test_bucketlist_models.sqlite")

    def test_create_bucketlist(self):
        self.assertEqual(
            app.config['created_bucketlist'].name,
            Bucketlist.query.filter_by(
                name=app.config['created_bucketlist'].name).one().name,
            msg="Cannot create bucket-list"
        )

    def test_update_bucketlist(self):
        current_bucketlist = Bucketlist.query.filter_by(
            name=app.config['created_bucketlist'].name).one()
        current_bucketlist.name = "My updated Bucketlist name"
        db.session.add(current_bucketlist)
        db.session.commit()

        self.assertEqual(
            "My updated Bucketlist name",
            Bucketlist.query.filter_by(
                name=current_bucketlist.name).one().name
        )

    def test_create_bucketlist_item(self):
        self.assertEqual(
            app.config['bucketlist_item'].name,
            BucketlistItems.query.filter_by(
                name=app.config['bucketlist_item'].name).one().name,
            msg="Cannot create bucket-list item"
        )

    def test_update_bucketlist_item(self):
        current_bucketlist_item = BucketlistItems.query.filter_by(
            name=app.config['bucketlist_item'].name).one()
        current_bucketlist_item.name = "Updated Bucketlist item name"
        db.session.add(current_bucketlist_item)
        db.session.commit()

        self.assertEqual(
            "Updated Bucketlist item name",
            BucketlistItems.query.filter_by(
                name=current_bucketlist_item.name).one().name
        )

    def test_zdelete_bucketlist_item(self):
        current_bucketlist_item = BucketlistItems.query.one()
        db.session.delete(current_bucketlist_item)
        db.session.commit()

        self.assertEqual(
            len(BucketlistItems.query.all()),
            0
        )

    def test_zdelete_bucketlist(self):
        current_bucketlist = Bucketlist.query.filter_by(
            name=app.config['created_bucketlist'].name).one()
        db.session.delete(current_bucketlist)
        db.session.commit()

        self.assertEqual(
            len(Bucketlist.query.all()),
            0
        )


if __name__ == '__main__':
    unittest.main()
