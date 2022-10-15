from ....models.booking_models import AllBooking, EventDay, MyService, ServiceEvent, EventSetting
from setting_web import db
from sqlalchemy import between
from ..event_ns.queries import find_boundaries_week

from .validate import FilterBooking as Filter, FreedomBooking as FrBooking, AnswerCalendar
from .schema import InfoBookingSchema, EventDaySchema, EventDayCorrectDateSchema

import json
from datetime import datetime, timedelta, time, date

def _base_query():
    """Базовый запрос"""
    booking = AllBooking.query
    return booking


def get_all_booking():
    """Все записи"""
    all_booking = _base_query()
    api_all_booking_schema = InfoBookingSchema(many=True)

    return api_all_booking_schema.dump(all_booking)

def get_all_event():
    now_date = datetime.now()
    query_event = EventDay.query.filter(EventDay.day_start >= date(year=now_date.year, month=now_date.month, day=now_date.day))

    api_all_event = EventDaySchema(many=True)
    return api_all_event.dump(query_event)


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


def get_indo_calendar(cor_date: Filter):
    """Calendar Booking"""

    answer_calendar = []
    start_end_weeks, all_week = find_boundaries_week(cor_date.this_date_filter)
    try:
        for one_day in all_week:
            cor_date.this_date_filter = one_day
            one_answer_booking = AnswerCalendar(day=one_day.strftime('%Y-%m-%d'),
                                                event_day=find_booking_this_day(one_day))

            answer_calendar.append(json.loads(one_answer_booking.json()))
    except:
        print("error: fun in get_indo_calendar")
        return None, 404

    return answer_calendar


def find_intervals(intervals_list, all_booking_this_ev):
    print(all_booking_this_ev)
    for one_booking in all_booking_this_ev:
        for iter_interval in range(len(intervals_list)):
            if one_booking.time_start >= intervals_list[iter_interval][0] and one_booking.time_end <= \
                    intervals_list[iter_interval][1]:
                left_intervals = [intervals_list[iter_interval][0], one_booking.time_start]
                right_intervals = [one_booking.time_end, intervals_list[iter_interval][1]]

                intervals_list.pop(iter_interval)

                if left_intervals[0] != left_intervals[1]:
                    intervals_list.append(left_intervals)
                if right_intervals[0] != right_intervals[1]:
                    intervals_list.append(right_intervals)
                break

    return intervals_list


def fraction_window(intervals_list, info_service):
    if info_service.duration is not None and info_service.duration != time(hour=0, minute=0, second=0):
        drop_interval_list = []
        for one_window in intervals_list:
            delta_duration = timedelta(hours=info_service.duration.hour,
                                       minutes=info_service.duration.minute)

            print(one_window)
            new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

            while one_window[1] > new_window.time():
                print(one_window, new_window)
                drop_interval_list.append([(one_window[0]),
                                           new_window.time()])
                one_window[0] = new_window.time()
                new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

        intervals_list = drop_interval_list

    return intervals_list


def start_intervals_day(event_day: EventDay, tracer_day: date =None):
    if event_day.day_start == event_day.day_end and tracer_day is None:
        return [[event_day.event_time_start, event_day.event_time_end]]
    elif tracer_day is not None:
        if event_day.day_start < tracer_day < event_day.day_end:
            return [[time(hour=0), time(hour=23, minute=59)]]
        elif event_day.day_start == tracer_day:
            return [[event_day.event_time_start, time(hour=23, minute=59)]]
        elif event_day.day_end == tracer_day:
            return [[time(hour=0), event_day.event_time_end]]


def find_freedom_booking(name_service):
    con_ser_event = ServiceEvent.event_search_by_service(name_service)
    info_service = MyService.find_by_name(name_service)

    all_event_id = []
    answer = []

    now_date = datetime.now()
    this_day = date(year=now_date.year, month=now_date.month, day=now_date.day)

    # try:
    for one_q in con_ser_event:
        all_event_id.append(one_q.event_id)

    query_event = EventDay.query
    info_events = query_event.filter(db.and_(EventDay.event_setting_id.in_(all_event_id),
                                             db.or_(EventDay.day_start >= this_day,
                                             between(this_day, EventDay.day_start, EventDay.day_end)))).all()
    info_booking = AllBooking.find_booking_by_event_id(all_event_id)

    for one_event in info_events:
        all_booking_this_ev = info_booking.filter(AllBooking.signup_event == one_event.id).all()

        if one_event.day_start < one_event.day_end:
            start_iteration_day = one_event.day_start
            if this_day > one_event.day_start:
                start_iteration_day = this_day

            delta_days = one_event.day_end - start_iteration_day
            for iter_day in range(delta_days.days + 1):
                intervals_list = start_intervals_day(one_event, tracer_day=start_iteration_day + timedelta(days=iter_day))
                interval_time = {"day": start_iteration_day + timedelta(days=iter_day),
                                 "intervals": intervals_list}

                intervals_list = find_intervals(intervals_list, all_booking_this_ev)
                intervals_list = fraction_window(intervals_list, info_service)

                interval_time["intervals"] = intervals_list
                answer.append(interval_time)

        elif one_event.day_start == one_event.day_end:
            intervals_list = start_intervals_day(one_event)

            intervals_list = find_intervals(intervals_list, all_booking_this_ev)
            intervals_list = fraction_window(intervals_list, info_service)

            interval_time = {"day": one_event.day_start, "intervals": intervals_list}

            intervals_list = find_intervals(intervals_list, all_booking_this_ev)
            intervals_list = fraction_window(intervals_list, info_service)

            interval_time["intervals"] = intervals_list
            answer.append(interval_time)

    new_answer = []
    for one_window in answer:
        new_answer.append(json.loads(FrBooking(**one_window).json()))
    # except TypeError:
    #     return {"message": "not find this service"}, 404

    return new_answer, 200




