from ....models.booking_models import *

from calendar import Calendar
from datetime import datetime

from .schema import ServiceEvent, EventSettingSchema, EventDayCorrectDateSchema
from .validate import FilterEvent as Filter

now_date = datetime.now()
cl = Calendar()


def _base_query():
    query = EventSetting.query
    return query


def _base_query_se():
    query = db.session.query(ServiceEvent.quantity, MyService.name_service, EventSetting.name_event, EventSetting.day_start_g)
    query = query.join(MyService)
    query = query.join(EventSetting)
    return query


def all_working_date():
    """Все записи"""
    all_date = _base_query()
    api_all_work_date = EventSettingSchema(many=True)

    return api_all_work_date.dump(all_date)

def find_booking_this_day(dat: date):
    all_booking_service = EventDay.query
    between_date_start = EventDay.day_start.between(dat, dat)
    between_date_end = EventDay.day_end.between(dat, dat)

    res_query_sql = all_booking_service.filter(db.or_(between_date_start, between_date_end))
    res_query = res_query_sql.subquery() # фильтрация для дней

    cs_start = db.case([(db.and_(res_query.c.day_end == dat, res_query.c.day_start != res_query.c.day_end), time(hour=0)),
                        (db.and_(res_query.c.day_end < dat, res_query.c.day_start > dat), time(hour=0))],
                       else_=res_query.c.event_time_start).label("correct_time_start")

    cs_end = db.case([(db.and_(res_query.c.day_start == dat, res_query.c.day_start != res_query.c.day_end), time(hour=23, minute=59)),
                      (db.and_(res_query.c.day_end < dat, res_query.c.day_start > dat), time(hour=23, minute=59))],
                     else_=res_query.c.event_time_end).label("correct_time_end")

    res_query = db.session.query(res_query, EventDay, cs_start, cs_end).join(EventDay, res_query.c.id == EventDay.id)

    api_all_booking_schema = EventDayCorrectDateSchema(many=True)
    return api_all_booking_schema.dump(res_query)


def get_filter_work_day(filter_event: Filter):
    """Фильтры на каждое поле события"""
    this_day = _base_query()

    if filter_event.id is not None and len(filter_event.id) > 0:
        this_day = this_day.filter(EventSetting.name_event.in_(filter_event.id))

    # if filter_event.name is not None and len(filter_event.name) > 0:
    #     this_day = this_day.filter(Event.name_event.in_(filter_event.name))
    #
    # if filter_event.day_start:
    #     this_day = this_day.filter(Event.day_start >= filter_event.day_start)
    #
    # if filter_event.day_end:
    #     this_day = this_day.filter(Event.day_end <= filter_event.day_end)
    #
    # if filter_event.start_time:
    #     this_day = this_day.filter(Event.start_event >= filter_event.start_time)
    #
    # if filter_event.end_time:
    #     this_day = this_day.filter(Event.end_event >= filter_event.end_time)

    api_all_work_date = EventSettingSchema(many=True)
    return api_all_work_date.dump(this_day)


def check_exit_event(this_ck_date):
    """Проверка на существования услуги в эту дату"""
    ck_all_date = _base_query()
    status = ck_all_date.filter_by(EventSetting.day_start_g == this_ck_date).first() is not None

    return status


def weeks_in_all_event(name_service=None):
    """Дни, когда активна услуга"""
    all_data = _base_query_se()
    weeks_day = []

    for work_day in all_data:
        if work_day.name_service == name_service and work_day.day not in weeks_day:
            weeks_day.append(work_day.day)

    return weeks_day