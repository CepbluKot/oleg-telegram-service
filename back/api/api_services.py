from flask import jsonify, request
from main import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days, DaysShema
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


_base_query = db.session.query(MyService)


class InfoServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_service', 'price_service', 'name_staff')


@flask_app.route('/api/service/', methods=['Get'])
def all_service():
    all_service_data = _base_query
    api_all_booking_schema = InfoServiceSchema(many=True)

    return jsonify(api_all_booking_schema.dump(all_service_data))


@flask_app.route('/api/service/filter_name/<string:name_service>', methods=['GET'])
def filter_name(name_service):
    flt_service_data = _base_query
    flt_service_data = flt_service_data.filter(MyService.name_service == name_service)


@flask_app.route('/api/service/filter_staff/<string:name_staff>/', methods=['GET'])
@flask_app.route('/api/service/filter_staff/<string:name_staff>/<string:name_service>', methods=['GET'])
def filter_staff(name_staff, name_service=None):
    flt_service_data = _base_query

    query_staff_ar = db.session.query(MyStaff.service_staff).filter(MyStaff.name_staff == name_staff).all()
    service_staff = query_staff_ar[0][0]

    if name_service != None:
        flt_service_data = flt_service_data.filter(MyService.name_service == name_service)

    flt_service_data = flt_service_data.filter(MyService.id == db.any_(service_staff))
    api_all_booking_schema = InfoServiceSchema(many=True)

    return jsonify(api_all_booking_schema.dump(flt_service_data))
