from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'pop'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/system_control'

db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from models.days_coonecta import Days
from models.all_users_this_connecta import CompanyUsers
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.booking_date_connecta import AllBooking
from models.all_users_connectall import UsersConnectALL
db.init_app(flask_app)
migrate.init_app(flask_app, db)

if __name__ == 'back.app':
    flask_app.run(debug=True)