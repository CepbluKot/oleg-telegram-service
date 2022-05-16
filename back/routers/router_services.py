from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_services import *

@flask_app.route('/api/service/', methods=['GET'])
def all_service_web():
    res_data = all_service()
    return jsonify(res_data)


@flask_app.route('/api/service/filter_staff/<string:name_staff>/', methods=['GET'])
@flask_app.route('/api/service/filter_staff/<string:name_staff>/<string:name_service>', methods=['GET'])
def filter_staff(name_staff, name_service=None):
    res_data = get_filter_services(name_staff=name_staff, name_service=name_service)
    return jsonify(res_data)
