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
cl = Calendar()


def _base_query():
    query = db.session.query(Days).filter(Days.day > date(year=now_date.year, month=now_date.month, day=now_date.day))
    return query

class InfoDaysWorkingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'day', 'service_this_day', 'staff_free')


def all_working_date():
    all_date = _base_query()

    api_all_work_date = InfoDaysWorkingSchema(many=True)
    return api_all_work_date.dump(all_date)


def check_exit_day(this_ck_date):
    ck_all_date = _base_query()
    status = ck_all_date.filter_by(Days.day == this_ck_date).first() is not None

    return status


def get_filter_work_day(check_day=None, name_service=None, between_start=None, between_end=None):
    this_day = _base_query()

    if name_service:
        this_day = this_day.filter(Days.service_this_day.op('->')(name_service) != None)

    if check_day:
        this_day = this_day.filter(Days.day == check_day)

    if between_start and between_end and not check_day:
        this_day = this_day.filter(Days.day.between(between_start, between_end))

    api_all_work_date = InfoDaysWorkingSchema(many=True)
    return api_all_work_date.dump(this_day)



def find_boundaries_week(day):
    mycal = cl.monthdatescalendar(day.year, day.month)
    start_end_week = []

    for week in mycal:
        if day in week:
            start_end_week.append(week[0])
            start_end_week.append(week[-1])

            if start_end_week not in day:
                day.append(start_end_week)
            break
    return start_end_week


def weeks_in_all_date(name_service=None):
    all_date = _base_query().all()
    weeks_day = []

    for work_day in all_date:
        if not name_service and work_day.service_this_day.get(name_service):
            continue
        weeks_day.append(work_day.day)

    return weeks_day