from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers

from api.api_services import _base_query


def update_service(old_name, new_name=None, new_price=None):
    service = _base_query().filter(MyService.name_service == old_name)

    if new_name is not None:
        service.name_service = new_name

    if new_price is not None:
        service.price_service = new_price
    db.session.commit()
