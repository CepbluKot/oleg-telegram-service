from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_client_company import *
from bissnes_logic.update_data.update_client import update_data_client


@flask_app.route('/api/client/', methods=['GET'])
def all_cl_web():
    res_data = all_client()
    return jsonify(res_data)


@flask_app.route('/api/client/filter/<int:tg_id>/', methods=['GET', 'PUT'])
def client_info_tg_web(tg_id):
    if request.method == 'PUT':
        new_name = request.json.get("new_name", None)
        new_phone_num = request.json.get("new_phone_new", None)
        update_data_client(tg_id, new_name, new_phone_num)

    res_data = get_filter_client(tg_id=tg_id)
    return jsonify(res_data)


@flask_app.route('/api/client/register', methods=['POST'])
def reg_us_web():
    tg_id = request.json.get("tg_id", None)
    name = request.json.get("name", None)
    phone = request.json.get("phone", None)

    try:
        add_new_us(tg_id, name, phone)
        return jsonify("Successful registration")
    except:
        return jsonify('Failed to register')