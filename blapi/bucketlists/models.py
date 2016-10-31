from app import db
from blapi.authorization.models import User


class Bucketlist(db.Model):
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship(User)


class BucketlistItems(db.Model):
    __tablename__ = 'bucketlistitems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())
    done = db.Column(db.Boolean())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    bucketlist = db.relationship(Bucketlist)
