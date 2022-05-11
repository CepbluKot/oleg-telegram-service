from flask import jsonify, request
from setting_web import flask_app, db, ma, cross_origin
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers

from calendar import Calendar
from datetime import date, datetime
from sqlalchemy import func

now_date = datetime.now()
_base_query = db.session.query(Days).filter(Days.day > date(year=now_date.year, month=now_date.month, day=now_date.day))


class InfoDaysWorkingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'day', 'free_items', 'staff_free')


def all_working_date():
    all_date = _base_query

    api_all_work_date = InfoDaysWorkingSchema(many=True)
    return api_all_work_date.dump(all_date)


def work_date_service(check_day=None, name_service=None, between_start=None, between_end=None):
    this_day = _base_query

    if name_service:
        this_day = this_day.filter(Days.service_this_day.op('->')(name_service) != None)

    if check_day:
        this_day = this_day.filter(Days.day == check_day)

    if between_start and between_end and not check_day:
        this_day = this_day.filter(Days.day.between(between_start, between_end))

    api_all_work_date = InfoDaysWorkingSchema(many=True)
    return api_all_work_date.dump(this_day)


def weeks_in_all_date(name_service=None):
    all_date = _base_query.all()
    weeks_day = []

    cl = Calendar()
    for work_day in all_date:
        if not name_service and work_day.service_this_day.get(name_service):
            continue

        mycal = cl.monthdatescalendar(work_day.day.year, work_day.day.month)
        start_end_week = []

        for week in mycal:
            if work_day.day in week:
                start_end_week.append(week[0])
                start_end_week.append(week[-1])

                if start_end_week not in weeks_day:
                    weeks_day.append(start_end_week)
                break

    return weeks_day

