from setting_web import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


def _base_query():
    res_query = db.session.query(MyService)
    return res_query


class InfoServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_service', 'price_service', 'name_service', 'name_staff')


def all_service():
    all_service_data = _base_query()
    api_all_booking_schema = InfoServiceSchema(many=True)

    return api_all_booking_schema.dump(all_service_data)


def get_filter_services(name_staff=None, name_service=None):
    data_services = _base_query()

    if name_service != None:
        data_services = data_services.filter(MyService.name_service == name_service)

    if name_staff != None:
        query_staff_ar = db.session.query(MyStaff.service_staff).filter(MyStaff.name_staff == name_staff).all()
        service_staff = query_staff_ar[0][0]

        data_services = data_services.filter(MyService.id == db.any_(service_staff))

    api_all_booking_schema = InfoServiceSchema(many=True)
    return api_all_booking_schema.dump(data_services)

