from flask import jsonify, request
from main import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days, DaysShema
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


class InfoBookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'time', 'name_client', 'tg_id', 'phone_num', 'name_staff', 'name_service', 'day')


def _base_query():
    booking = db.session.query(AllBooking.id, AllBooking.time, CompanyUsers.name_client, CompanyUsers.tg_id,
                               CompanyUsers.phone_num, MyStaff.name_staff, MyService.name_service, Days.day)
    booking = booking.join(CompanyUsers)
    booking = booking.join(Days)
    booking = booking.join(MyService)
    booking = booking.join(MyStaff)

    return booking


@flask_app.route('/api/booking/', methods=['GET'])
def get_all_booking():
    all_booking = _base_query()
    api_all_booking_schema = InfoBookingSchema(many=True)

    return jsonify(api_all_booking_schema.dump(all_booking))


@flask_app.route('/api/booking/filter_date/<string:my_date>/', methods=['GET'])
@flask_app.route('/api/booking/filter_date/<string:my_date>/<int:g_time_start>&<int:g_time_end>', methods=['GET'])
def get_info_date_booking(my_date, g_time_start=None, g_time_end=None):
    this_date = datetime.strptime(my_date, '%Y-%m-%d').date()
    one_day_booking = _base_query()

    if g_time_start != None and g_time_end != None:
        time_start = time(hour=g_time_start)
        time_end = time(hour=g_time_end)
        one_day_booking = one_day_booking.filter(db.and_(Days.day == this_date, AllBooking.time.between(time_start, time_end)))

        print(one_day_booking)
    else:
        one_day_booking = one_day_booking.filter(Days.day == this_date)

    print(one_day_booking)
    api_all_booking_schema = InfoBookingSchema(many=True)
    return jsonify(api_all_booking_schema.dump(one_day_booking))


@flask_app.route('/api/booking/filter_service/<string:my_service>', methods=['GET'])
@flask_app.route('/api/booking/filter_service/<string:my_service>/<string:my_date>', methods=['GET'])
def get_info_service_booking(my_service, my_date=None):
    print(my_service)
    all_booking_service = _base_query()
    all_booking_service = all_booking_service.filter(MyService.name_service == my_service)

    if my_date != None:
        this_date = datetime.strptime(my_date, '%Y-%m-%d').date()
        all_booking_service = all_booking_service.filter(db.and_(MyService.name_service == my_service, Days.day == this_date))

    api_all_booking_schema = InfoBookingSchema(many=True)
    return jsonify(api_all_booking_schema.dump(all_booking_service))

