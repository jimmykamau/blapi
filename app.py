import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


from blapi.authorization.endpoints import \
    Registration, authenticate, identity
from blapi.bucketlists.endpoints import \
    BucketlistControl, BucketlistItemControl


jwt = JWT(app, authenticate, identity)


api.add_resource(
    Registration, '/auth/register', '/auth/register/<user_id>')
api.add_resource(
    BucketlistControl, '/bucketlists', '/bucketlists/<bucketlist_id>')
api.add_resource(
    BucketlistItemControl, '/bucketlists/<bucketlist_id>/items/')


if __name__ == '__main__':
    app.run()
