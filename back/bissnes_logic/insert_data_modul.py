from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers

from api.api_workig_date import work_date_service
from api.api_services import get_filter_services
from api.api_client_company import client_info_tg

from bissnes_logic.calendar_logic import freedom_items

from datetime import date

def add_booking(info_booking):
    status = freedom_items(info_booking["service"], info_booking["day"], info_booking["time_start"])

    if status == "Error":
        return status

    day_id = work_date_service(check_day=info_booking["day"])[0]["id"]
    service_id = get_filter_services(name_service=info_booking["service"])[0]["id"]
    user_id = client_info_tg(tg_id=info_booking["tg_id"])["id"]

    new_us = AllBooking(day_id, user_id, service_id, info_booking["time_start"], info_booking["time_end"])
    db.session.add(new_us)
    db.session.commit()