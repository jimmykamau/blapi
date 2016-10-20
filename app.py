import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


from blapi.authorization.endpoints import Registration, Login


api.add_resource(
    Registration, '/auth/register', '/auth/register/<user_id>')
api.add_resource(
    Login, '/auth/login')

if __name__ == '__main__':
    app.run()
