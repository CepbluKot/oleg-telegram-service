from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_booking import *

@flask_app.route('/api/booking/', methods=['GET', 'POST'])
@auth.admin_required()
def all_booking_web():
    if request.method == 'POST':
        data_booking = request.get_json()
        """"""

    res_data = get_all_booking()
    return jsonify(res_data)


@flask_app.route('/api/booking/filter/<string:my_date>/', methods=['GET'])
@flask_app.route('/api/booking/filter/<string:my_date>/<string:my_service>', methods=['GET'])
@flask_app.route('/api/booking/filter/<string:my_date>/<string:my_service>/<int:g_time_start>&<int:g_time_end>', methods=['GET'])
def get_info_date_booking_web(my_date, g_time_start=None, g_time_end=None):
    res_data = get_filter_booking(my_date, g_time_start, g_time_end)
    return jsonify(res_data)
