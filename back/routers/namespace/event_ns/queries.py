from setting_web import db, ma
from models.all_models import *

from calendar import Calendar
from datetime import date, datetime

from .schema import ServiceEvent, EventSchema

now_date = datetime.now()
cl = Calendar()


def _base_query():
    query = Event.query.filter(Event.day > date(year=now_date.year, month=now_date.month, day=now_date.day))
    return query


def _base_query_se():
    query = db.session.query(ServiceEvent.quantity, MyService.name_service, Event.name_event, Event.day)
    query = query.join(MyService)
    query = query.join(Event)
    return query


def all_working_date():
    """Все записи"""
    all_date = _base_query().all()
    api_all_work_date = EventSchema(many=True)

    return api_all_work_date.dump(all_date)


def get_filter_work_day(name_event=None,
                        check_day=None,
                        between_start=None,
                        between_end=None):

    this_day = _base_query()

    if name_event:
        this_day = this_day.filter(Event.name_event == name_event)

    if check_day:
        this_day = this_day.filter(Event.day == check_day)

    if (between_start and between_end and not check_day) and between_end >= between_start:
        this_day = this_day.filter(Event.day.between(between_start, between_end))

    api_all_work_date = EventSchema(many=True)
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


def check_exit_event(this_ck_date):
    ck_all_date = _base_query()
    status = ck_all_date.filter_by(Event.day == this_ck_date).first() is not None

    return status


def weeks_in_all_event(name_service=None):
    """Дни, когда активна услуга"""
    all_data = _base_query_se()
    weeks_day = []

    for work_day in all_data:
        print(work_day, work_day.name_service)
        if work_day.name_service == name_service and work_day.day not in weeks_day:
            weeks_day.append(work_day.day)

    return weeks_day