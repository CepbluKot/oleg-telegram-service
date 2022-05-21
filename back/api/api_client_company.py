from flask import jsonify, request
from setting_web import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


class InfoUsersComSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_client', 'tg_id', 'phone_num')


def _base_query():
    client = db.session.query(CompanyUsers)
    return client


def all_client():
    all_client_data = _base_query()
    api_all_client_schema = InfoUsersComSchema(many=True)
    return api_all_client_schema.dump(all_client_data)


def get_filter_client(name=None, tg_id=None, phone_num=None):
    client_data = _base_query()

    if tg_id is not None:
        client_data = client_data.filter(CompanyUsers.tg_id == tg_id)

    if phone_num is not None:
        client_data = client_data.filter(CompanyUsers.phone_num == phone_num)

    if (name is not None) and (tg_id is not None or phone_num is not None):
        client_data = client_data.filter(CompanyUsers.name_client == name)

    api_client_schema = InfoUsersComSchema()
    return api_client_schema.dump(client_data)


def check_exit_us(tg_id=None):
    client_data = _base_query()
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first() is not None

    return client_data

