from main import ModelView, db, admin, flask_app, Migrate
import admin_tools

import api.api_booking
import api.api_services
import api.api_authentication

migrate = Migrate(flask_app, db)

from models.days_coonecta import Days
from models.all_users_this_connecta import CompanyUsers
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.booking_date_connecta import AllBooking
from models.all_users_connectall import UsersConnectALL


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)