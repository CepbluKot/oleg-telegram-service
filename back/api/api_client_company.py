from flask import jsonify, request
from setting_web import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


_base_query = db.session.query(CompanyUsers)


class InfoUsersComSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_client', 'tg_id', 'phone_num')


def all_client():
    all_client_data = _base_query
    api_all_client_schema = InfoUsersComSchema(many=True)
    return api_all_client_schema.dump(all_client_data)


def client_info_tg(tg_id):
    client_data = _base_query
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first()

    api_client_schema = InfoUsersComSchema()
    return api_client_schema.dump(client_data)


def client_info_phonenum(phone_num):
    client_data = _base_query
    client_data = client_data.filter(CompanyUsers.phone_num == phone_num).first()

    api_client_schema = InfoUsersComSchema()
    return api_client_schema.dump(client_data)


def add_new_us(tg_id, name, phone):
    new_us = CompanyUsers(name, tg_id, phone)
    db.session.add(new_us)
    db.session.commit()


def update_info_us(tg_id, name=None, phone=None):
    client_data = _base_query
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first()

    if name != None:
        client_data.name_client = name
    if phone != None:
        client_data.phone_num = phone

    db.session.commit()


def check_exit_us(tg_id):
    client_data = _base_query
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id)

    if client_data != None:
        return True
    return False


"""     W     E     B          A     P    I """


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