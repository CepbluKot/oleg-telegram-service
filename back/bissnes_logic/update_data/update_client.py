from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers

from api.api_client_company import _base_query


def update_data_client(tg_id, name=None, phone=None):
    client_data = _base_query()
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first()

    if name is not None:
        client_data.name_client = name
    if phone is not None:
        client_data.phone_num = phone
    db.session.commit()

