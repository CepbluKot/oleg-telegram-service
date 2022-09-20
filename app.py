from setting_web import db, flask_app, Migrate
migrate = Migrate(flask_app, db)

from back_users.models.all_models import *
from back.models.booking_models import *

