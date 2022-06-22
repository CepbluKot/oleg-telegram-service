from setting_web import db, flask_app, Migrate
migrate = Migrate(flask_app, db)

from models.all_models import *

