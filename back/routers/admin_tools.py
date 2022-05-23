from setting_web import ModelView, db, admin

from models.default_setting_users import DefaultSetting
from models.days_coonecta import Days
from models.all_users_this_connecta import CompanyUsers
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.booking_date_connecta import AllBooking
from models.all_users_connectall import UsersConnectALL

admin.add_view(ModelView(DefaultSetting, db.session))
admin.add_view(ModelView(Days, db.session))
admin.add_view(ModelView(CompanyUsers, db.session))
admin.add_view(ModelView(MyService, db.session))
admin.add_view(ModelView(MyStaff, db.session))
admin.add_view(ModelView(UsersConnectALL, db.session))
admin.add_view(ModelView(AllBooking, db.session))
