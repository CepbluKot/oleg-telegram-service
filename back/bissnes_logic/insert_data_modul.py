from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers
from models.all_users_connectall import UsersConnectALL

from api.api_workig_date import get_filter_work_day, check_exit_day
from api.api_services import get_filter_services, check_exit_service
from api.api_client_company import get_filter_client

from bissnes_logic.calendar_logic import freedom_items
from bissnes_logic.validators import RegisterUserConnectA, RegisterСlient
from pydantic import ValidationError

from datetime import date, time, datetime
from werkzeug.security import generate_password_hash, check_password_hash



"""     USERS - CONNECTA     """


def add_users_connecta(password, username, name):
    try:
        RegisterUserConnectA(name=name, username=username, password=password)
    except ValidationError as error:
        return error.json(indent=5)

    hash_password = generate_password_hash(password)
    new_user = UsersConnectALL(name, username, hash_password)
    db.session.add(new_user)
    db.session.commit()

    return "successful registration"


"""    CLIENT     """


def add_new_us(tg_id, name, phone):
    try:
        RegisterСlient(name=name, phone=phone)
    except ValidationError as error:
        return error.json(indent=5)

    new_us = CompanyUsers(name, tg_id, phone)
    db.session.add(new_us)
    db.session.commit()

    return "successful add client"


"""   BOOKING    """


def add_booking(info_booking: dict):
    """Добавление новой брони"""
    """info_booking = { "service": name, "day": date, "time_start": time, "time_end": time, "tg_id": id(int) }"""
    status = freedom_items(info_booking["service"], info_booking["day"], info_booking["time_start"])

    if status == "Error":
        return status

    day_id = get_filter_work_day(check_day=info_booking["day"])[0]["id"]
    service_id = get_filter_services(name_service=info_booking["service"])[0]["id"]
    user_id = get_filter_client(tg_id=info_booking["tg_id"])["id"]

    new_us = AllBooking(day_id, user_id, service_id, info_booking["time_start"], info_booking["time_end"])
    db.session.add(new_us)
    db.session.commit()
    return status


"""     WORK   DAYS     """

buffer_update_day = {}
buffer_add_day = {}


def add_work_day(days_add: list):
    for one_day in days_add:
        db.session.add(buffer_add_day[one_day])
    db.session.commit()


"""Составить стандартные настройки пользователя и создать таблицу для них
   продумать таблицу настроек(поля, типы данных), валидация pydantic"""


def preparation_insert_work_day(info_day: dict):
    """info_day = [{"day" : 2022-05-24, "service": {"okno": 5,...}},...]"""
    for one_day in info_day:
        exits = check_exit_day(one_day["day"])

        if exits:
            buffer_update_day[one_day["day"]] = one_day["service"]
        else:
            this_day = datetime.strptime(info_day["day"], '%Y-%m-%d').date()
            new_work_day = Days(this_day, info_day["service"])
            buffer_add_day[info_day["day"]] = new_work_day


"""   SERVICE    """


def add_service(name_service: str, price: float):
    """Добавление новой услуги"""
    new_service = MyService(name_service, price)
    db.session.add(new_service)
    db.session.commit()






