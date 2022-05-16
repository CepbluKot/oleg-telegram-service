from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_client_company import *


@flask_app.route('/api/client/', methods=['GET'])
def all_cl_web():
    res_data = all_client()
    return jsonify(res_data)


@flask_app.route('/api/client/filter_tg/<int:tg_id>/', methods=['GET'])
@flask_app.route('/api/client/filter_tg/<int:tg_id>/update/<string:new_name>_<string:new_phone_num>', methods=['PUT'])
def client_info_tg_web(tg_id, new_name=None, new_phone_num=None):
    if request.method == 'PUT':
        update_info_us(tg_id, new_name, new_phone_num)

    res_data = client_info_tg(tg_id)
    return jsonify(res_data)


@flask_app.route('/api/client/filter_phone/<int:phone_num>/', methods=['GET'])
def cl_info_ph_web(phone_num):
    res_data = client_info_phonenum(phone_num)
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