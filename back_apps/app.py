from setting_web import flask_app, db, Migrate, basedir
migrate = Migrate(flask_app, db, directory=basedir + '/migrations')
from back_users.models.all_models import *
from back.models.booking_models import *