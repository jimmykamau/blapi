from datetime import datetime
from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from app import db
from .models import Bucketlist, BucketlistItems
from .schemas import BucketlistSchema, BucketlistItemsSchema


bucketlist_schema = BucketlistSchema()
bucketlists_schema = BucketlistSchema(many=True)
bucketlist_item_schema = BucketlistItemsSchema()
bucketlist_items_schema = BucketlistItemsSchema(many=True)


def check_user_owns_bucketlist(current_user, bucketlist_id):
        try:
            Bucketlist.query.filter_by(
                created_by=current_user, id=bucketlist_id).one()
            return True
        except NoResultFound:
            return False


class BucketlistControl(Resource):

    @jwt_required()
    def get(self, bucketlist_id=False):
        try:
            bucketlists = Bucketlist.query.filter_by(
                created_by=int(str(current_identity)), id=bucketlist_id).all()\
                if bucketlist_id else Bucketlist.query.filter_by(
                created_by=int(str(current_identity))).all()
            bucketlists_result = bucketlists_schema.dump(bucketlists)
            return {'bucketlists': bucketlists_result}, 200
        except NoResultFound:
            abort(
                400,
                message="No bucket-list with {} as owner"
                .format(current_identity)
            )

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
    def put(self, bucketlist_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            json_data = request.get_json()
            if not json_data:
                abort(400, message="Empty request")

            data, errors = bucketlist_schema.load(json_data, partial=True)
            if errors:
                abort(422, message=errors)

            try:
                bucketlist = Bucketlist.query.filter_by(
                    created_by=int(str(current_identity)),
                    id=bucketlist_id).one()
                bucketlist.name = data['name']
                bucketlist.date_modified = datetime.utcnow()
                db.session.add(bucketlist)
                db.session.commit()
                modified_bucketlist = bucketlist_schema.dump(bucketlist)
                return {'bucketlist': modified_bucketlist}, 201
            except Exception as exception_message:
                abort(500, message=exception_message)
        else:
            abort(403,
                  message="User doesn't own bucketlist or " +
                  "bucketlist doesn't exist")

    @jwt_required()
    def delete(self, bucketlist_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            try:
                bucketlist_items = BucketlistItems.query.filter_by(
                    bucketlist_id=bucketlist_id).all()
                bucketlist = Bucketlist.query.filter_by(
                    created_by=int(str(current_identity)),
                    id=bucketlist_id).one()
                if len(bucketlist_items) != 0:
                    for bucketlist_item in bucketlist_items:
                        db.session.delete(bucketlist_item)
                db.session.delete(bucketlist)
                db.session.commit()
                return {'message': 'Bucket-list deleted successfully'}
            except Exception as exception_message:
                abort(500, message=exception_message)
        else:
            abort(403,
                  message="User doesn't own bucketlist or " +
                  "bucketlist doesn't exist")


class BucketlistItemControl(Resource):

    @jwt_required()
    def get(self, bucketlist_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            try:
                bucketlist_items = BucketlistItems.query.filter_by(
                    bucketlist_id=bucketlist_id).all()
                bucketlist_items_result = \
                    bucketlist_items_schema.dump(bucketlist_items)
                return {'bucketlist items': bucketlist_items_result}, 200
            except NoResultFound:
                abort(
                    400,
                    message="No bucket-list items for specified bucket-list")

    @jwt_required()
    def post(self, bucketlist_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            json_data = request.get_json()
            if not json_data:
                abort(400, message="Empty request")

            data, errors = bucketlist_item_schema.load(json_data, partial=True)
            if errors:
                abort(422, message=errors)

            try:
                new_bucketlist_item = BucketlistItems(
                    name=data['name'], date_created=datetime.utcnow(),
                    date_modified=datetime.utcnow(), done=data['done'],
                    bucketlist_id=int(bucketlist_id)
                )
                db.session.add(new_bucketlist_item)
                db.session.commit()
                created_bucketlist_item = \
                    bucketlist_item_schema.dump(new_bucketlist_item)
                return {
                    'bucketlist': created_bucketlist_item
                }, 201
            except Exception as exception_message:
                abort(500, message=exception_message)
        else:
            abort(403,
                  message="User doesn't own bucketlist or " +
                  "bucketlist doesn't exist")

    @jwt_required()
    def put(self, bucketlist_id, item_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            json_data = request.get_json()
            if not json_data:
                abort(400, message="Empty request")

            data, errors = bucketlist_item_schema.load(json_data)
            if errors:
                abort(422, message=errors)

            try:
                bucketlist_item = BucketlistItems.query.filter_by(
                    bucketlist_id=bucketlist_id, id=item_id).one()
                bucketlist_item.name = data['name']
                bucketlist_item.done = data['done']
                bucketlist_item.date_modified = datetime.utcnow()
                db.session.add(bucketlist_item)
                db.session.commit()
                modified_bucketlist_item = bucketlist_item_schema.dump(
                    bucketlist_item)
                return {'bucketlist': modified_bucketlist_item}, 201
            except Exception as exception_message:
                abort(500, message=exception_message)
        else:
            abort(403,
                  message="User doesn't own bucketlist or " +
                  "bucketlist doesn't exist")

    @jwt_required()
    def delete(self, bucketlist_id, item_id):
        if check_user_owns_bucketlist(
                int(str(current_identity)), bucketlist_id):
            try:
                bucketlist_item = BucketlistItems.query.filter_by(
                    bucketlist_id=bucketlist_id, id=item_id).one()
                db.session.delete(bucketlist_item)
                db.session.commit()
                return {'message': 'Bucket-list item deleted successfully'}
            except Exception as exception_message:
                abort(500, message=exception_message)
        else:
            abort(403,
                  message="User doesn't own bucketlist or " +
                  "bucketlist doesn't exist")
