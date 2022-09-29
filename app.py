from setting_web import head_conf, Migrate
migrate = Migrate(head_conf.flask_app, head_conf.db)

from back_users.models.all_models import *
from back.models.booking_models import *

