from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_booking import *

@flask_app.route('/api/booking/', methods=['GET', 'POST'])
#@auth.admin_required()
def all_booking_web():
    if request.method == 'POST':
        data_booking = request.get_json()
        

    res_data = get_all_booking()
    print(res_data)
    return jsonify(res_data)


@flask_app.route('/api/booking/filter/<string:my_date>/', methods=['GET'])
@flask_app.route('/api/booking/filter/calendar<string:date_start>&<string:date_stop>/', methods=['GET'])
@flask_app.route('/api/booking/filter/<string:my_date>/<string:my_service>', methods=['GET'])
@flask_app.route('/api/booking/filter/<string:my_date>/<string:my_service>/<int:g_time_start>&<int:g_time_end>', methods=['GET'])
def get_info_date_booking_web(my_date=None,  date_start=None, date_stop=None, my_service=None, g_time_start=None,
                              g_time_end=None):
    res_data = get_filter_booking(my_service, my_date, date_start, date_stop, g_time_start, g_time_end)
    return jsonify(res_data)


@flask_app.route('/api/booking/cal_select/<string:day_select>/', methods=['GET'])
def get_info_for_calendar(day_select=None):
    res_data = get_indo_calendar(day_select)
    return jsonify(res_data)

