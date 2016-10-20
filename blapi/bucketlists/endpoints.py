from datetime import datetime
from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from app import db
from .models import Bucketlist, BucketlistItems
from .schemas import BucketlistSchema, BucketlistItemsSchema


bucketlist_schema = BucketlistSchema()
bucketlist_items_schema = BucketlistItemsSchema()


class BucketlistControl(Resource):

    @jwt_required()
    def get(self):
        return {'user': str(current_identity)}, 200

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(400, message="Empty request")

        data, errors = bucketlist_schema.load(json_data)
        if errors:
            abort(422, message=errors)

        try:
            new_bucketlist = Bucketlist(
                name=data['name'], date_created=datetime.utcnow(),
                date_modified=datetime.utcnow(),
                created_by=int(str(current_identity))
            )
            db.session.add(new_bucketlist)
            db.session.commit()
            created_bucketlist = bucketlist_schema.dump(new_bucketlist)
            return {
                'bucketlist': created_bucketlist
            }, 201
        except Exception as exception_message:
            abort(500, message=exception_message)

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass


class BucketlistItemControl(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
