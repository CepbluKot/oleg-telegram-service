import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required

sys.path.append('/home/eliss/tg-helper/back/models')

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)

flask_app.config['FLASK_ENV'] = 'development'
flask_app.config['SECRET_KEY'] = 'pop'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/system_control'

flask_app.config['"JWT_SECRET_KEY'] = 'key-popov-gay'
jwt = JWTManager(flask_app)

db = SQLAlchemy(flask_app)
admin = Admin(flask_app)
ma = Marshmallow(flask_app)
