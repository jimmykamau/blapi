from app import db

from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())

    # Serialization for json requests
    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
        }

    # Representation of model
    def __repr__(self):
        return (self.id)
