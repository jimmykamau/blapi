from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, \
    check_password_hash

from app import db
from .models import User
from .schemas import UserSchema

user_schema = UserSchema()


def authenticate(username, password):
    user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


class Registration(Resource):

    def get(self, user_id):
        try:
            user = User.query.filter_by(id=user_id).one()
            user_result = user_schema.dump(user)
            return {'user': user_result}, 200
        except NoResultFound:
            abort(
                400, message="No user with id {}".format(user_id)
            )

    def post(self):
        json_data = request.get_json()

        if not json_data:
            abort(400, message="Empty request")

        data, errors = user_schema.load(json_data)
        if errors:
            abort(422, message=errors)

        try:
            password = generate_password_hash(data['password'])
            new_user = User(
                email=data['email'], password=password,
                full_name=data['full_name'], active=True
            )
            db.session.add(new_user)
            db.session.commit()
            return {
                'message': "{} created successfully".format(data['full_name'])
            }, 200
        except Exception:
            abort(403, message="User not created")
