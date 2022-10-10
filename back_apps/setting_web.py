import json
import sys
import os
from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required
from celery import Celery
import configparser
from flask_debugtoolbar import DebugToolbarExtension
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.dirname(__file__)) + '/conf_back.ini')

flask_app = Flask(__name__)


class HeadConfigApp:
    password_swag: str
    auth_setting_swagger: dict

    def __init__(self):
        global flask_app

        basedir = os.path.abspath(os.path.dirname(__file__))

        flask_app.debug = config['FLASK']['FLASK_DEBUG']
        flask_app.config['CORS_HEADERS'] = config['FLASK']['CORS_HEADERS']
        flask_app.config['FLASK_ENV'] = config['FLASK']['FLASK_ENV']
        flask_app.config['JSON_AS_ASCII'] = config['FLASK']['JSON_AS_ASCII']
        flask_app.config['SECRET_KEY'] = config['FLASK']['SECRET_KEY']

        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['FLASK']['SQLALCHEMY_TRACK_MODIFICATIONS']
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL",
                                                                config['FLASK']['SQLALCHEMY_DATABASE_URI'])

        flask_app.config['JWT_SECRET_KEY'] = config['JWT']['JWT_SECRET_KEY']
        flask_app.config['RESTX_MASK_SWAGGER'] = config['SWAGGER']['RESTX_MASK_SWAGGER']
        flask_app.config['SWAGGER_UI_JSONEDITOR'] = config['SWAGGER']['SWAGGER_UI_JSONEDITOR']

        flask_app.config['BASIC_AUTH_USERNAME'] = config['FLASK']['BASIC_AUTH_USERNAME']
        flask_app.config['BASIC_AUTH_PASSWORD'] = config['FLASK']['BASIC_AUTH_PASSWORD']
        flask_app.config["CELERY_BROKER_URL"] = config['REDIS']['ROUTER']
        flask_app.config["CELERY_RESULT_BACKEND"] = config['REDIS']['ROUTER']

        self.password_swag = config['SWAGGER']['PASSWORD_SWAGGER']
        self.auth_setting_swagger = eval(config['SWAGGER']['AUTH_PARAMETER'])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_input = None

        if 'X-API-KEY' in request.headers:
            token_input = request.headers['X-API-KEY']

        if not token_input:
            return {'message': 'Not have token, give me please'}

        if token_input != head_conf.password_swag:
            return {'message': 'token not correct'}, 403

        return f(*args, **kwargs)
    return decorated


head_conf = HeadConfigApp()

jwt = JWTManager(flask_app)
db = SQLAlchemy(flask_app)
ma = Marshmallow(flask_app)
admin = Admin(flask_app, name='OLEG')
CORS(flask_app)

celery_app = Celery(flask_app.name, broker=flask_app.config["CELERY_BROKER_URL"])
celery_app.conf.update(flask_app.config)
