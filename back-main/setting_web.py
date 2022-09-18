import sys
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required
import configparser

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

config = configparser.ConfigParser()
config.read('config_service.ini')

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)
CORS(flask_app, supports_credentials=True)

flask_app.config['CORS_HEADERS'] = 'application/json'
flask_app.config['FLASK_ENV'] = 'development'
flask_app.config['SECRET_KEY'] = 'pop'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/admin_control'

flask_app.config['JWT_SECRET_KEY'] = 'key-popov-gay'
flask_app.config['RESTPLUS_MASK_SWAGGER'] = False
flask_app.config['SWAGGER_UI_JSONEDITOR'] = True
jwt = JWTManager(flask_app)

db = SQLAlchemy(flask_app)
ma = Marshmallow(flask_app)

flask_app.config['BASIC_AUTH_USERNAME'] = 'popov'
flask_app.config['BASIC_AUTH_PASSWORD'] = 'gay'

admin = Admin(flask_app, name='OLEG')