from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Event
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers


from api.api_workig_date import _base_query
from bissnes_logic.insert_data_modul import buffer_update_day


def update_buffer_day(days: list):
    for one_day in days:
        this_day = datetime.strptime(one_day, '%Y-%m-%d').date()
        query_day = _base_query().filter(Event.day == this_day)

        query_day.service_this_day = buffer_update_day[one_day]

    db.session.commit()


def update_work_day(info_days: dict):
    """info_days = {"day": 2022-05-24, "update_service" = {"service_name1": n, .....}}"" """
    for one_day in info_days:
        this_day = datetime.strptime(info_days["day"], '%Y-%m-%d').date()
        query_day = _base_query().filter(Event.day == this_day)
        #это апи а не запрос

        for service_upd, quantity in info_days["update_service"].items():
            query_day.service_this_day[service_upd] = quantity

    db.session.commit()
