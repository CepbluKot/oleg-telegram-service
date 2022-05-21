from flask import jsonify, request
from setting_web import flask_app, db, ma

#api
from api.api_services import *

#bissnes_logic
from bissnes_logic.insert_data_modul import add_service


#forms
from forms.insert_forms import ServiceAddForm


@flask_app.route('/api/service/', methods=['GET', 'POST'])
def all_service_web():

    if request.method == 'POST':
        name_service = request.json.get("name_us", None)
        price_service = request.json.get("price", None)
        add_service(name_service, price_service)

    res_data = all_service()
    return jsonify(res_data)

@flask_app.route('/api/service/filter_staff/<string:name_staff>/', methods=['GET'])
@flask_app.route('/api/service/filter_staff/<string:name_staff>/<string:name_service>', methods=['GET'])
def filter_staff(name_staff, name_service=None):
    res_data = get_filter_services(name_staff=name_staff, name_service=name_service)
    return jsonify(res_data)
