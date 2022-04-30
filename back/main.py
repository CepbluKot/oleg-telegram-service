import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

sys.path.append('/home/eliss/tg-helper/back/models')

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)

flask_app.config['FLASK_ENV'] = 'development'
flask_app.config['SECRET_KEY'] = 'pop'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/system_control'

db = SQLAlchemy(flask_app)
admin = Admin(flask_app)
ma = Marshmallow(flask_app)
