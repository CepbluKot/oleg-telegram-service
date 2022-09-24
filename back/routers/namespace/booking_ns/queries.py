from back.models.booking_models import *
from back.routers.namespace.event_ns.queries import find_boundaries_week
from operator import ge, le
import orjson

from .validate import FilterBooking as Filter, FreedomBooking as FrBooking, AnswerCalendar
from .schema import InfoBookingSchema, EventSchema

import json
from datetime import datetime, timedelta, time

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
    query_event = Event.query.filter(Event.day_end >= date(year=now_date.year, month=now_date.month, day=now_date.day))

    api_all_event = EventSchema(many=True)
    return api_all_event.dump(query_event)


def find_booking_this_day(dat: date):
    all_booking_service = Event.query.join(AllBooking).filter(db.and_(AllBooking.day_booking == dat))

    between_date = Event.day_start.between(dat, dat)
    single_date = all_booking_service.filter(between_date)
    many_date = all_booking_service.filter(Event.many_day is not None)
    many_date = many_date.filter(Event.many_day.any(dat, operator=le))

    all_booking_service = single_date.union(many_date)
    api_all_booking_schema = EventSchema(many=True)

    return api_all_booking_schema.dump(all_booking_service)

def get_filter_booking(new_filter: Filter):
    all_booking_service = _base_query()

    """Filter about people"""
    if new_filter.clients_tg_id_filter is not None:
        if new_filter.clients_tg_id_filter.tg_id is not None:
            all_booking_service = all_booking_service.filter(CompanyUsers.tg_id.in_(new_filter.clients_tg_id_filter.tg_id))

        if new_filter.clients_tg_id_filter.phone_num is not None:
            all_booking_service = all_booking_service.filter(CompanyUsers.phone_num.in_(new_filter.clients_tg_id_filter.phone_num))

        if new_filter.clients_tg_id_filter.name is not None:
            all_booking_service = all_booking_service.filter(CompanyUsers.name_client.in_(new_filter.clients_tg_id_filter.name))

    """Filter about service"""
    if new_filter.service_filter is not None:
        all_booking_service = all_booking_service.filter(MyService.name_service == new_filter.service_filter)

    """Filter about Date and Time"""
    if new_filter.this_date_filter is not None:
        all_booking_service = all_booking_service.filter(AllBooking.day_booking == new_filter.this_date_filter)

    if (new_filter.date_start_filter is not None) and (new_filter.date_end_filter is not None) \
            and (new_filter.this_date_filter is None):
        between_date = Event.day_start.between(new_filter.date_start_filter, new_filter.date_end_filter)
        single_date = all_booking_service.filter(between_date)

        many_date = all_booking_service.filter(Event.many_day is not None)
        many_date = many_date.filter(Event.many_day.any(new_filter.date_start_filter, operator=le))

        all_booking_service = single_date.union(many_date)

    if new_filter.time_start_filter is not None and new_filter.time_end_filter is not None:
        between_time = AllBooking.time_start.between(new_filter.time_start_filter, new_filter.time_end_filter)
        all_booking_service = all_booking_service.filter(between_time)

    all_booking_service = all_booking_service.order_by(db.desc(AllBooking.time_start))
    api_all_booking_schema = InfoBookingSchema(many=True)

    return api_all_booking_schema.dump(all_booking_service)


def get_indo_calendar(cor_date: Filter):
    """Calendar Booking"""

    answer_calendar = [] #example = [{day: "2022-01-22", booking = {}}, ]
    start_end_weeks, all_week = find_boundaries_week(cor_date.this_date_filter)
    try:
        for one_day in all_week:
            cor_date.this_date_filter = one_day
            one_answer_booking = AnswerCalendar(day=one_day.strftime('%Y-%m-%d'),
                                                booking=find_booking_this_day(one_day))

            answer_calendar.append(json.loads(one_answer_booking.json()))
    except:
        print("error: fun in get_indo_calendar")
        return None, 404

    return answer_calendar


def find_freedom_booking(name_service):
    con_ser_event = ServiceEvent.event_search_by_service(name_service)
    info_service = MyService.find_by_name(name_service)

    all_event_id = []
    answer = []

    try:
        for one_q in con_ser_event:
            all_event_id.append(one_q.event_id)

        now_date = datetime.now()
        info_events = Event.query.filter(db.and_(Event.id.in_(all_event_id),
                                           Event.day_end >= date(year=now_date.year, month=now_date.month, day=now_date.day))).all()

        info_booking = AllBooking.find_booking_by_event_id(all_event_id)

        for one_event in info_events:
            "Подготовка апи для одного события"
            if one_event.weekdays is None or len(one_event.weekdays) == 0:
                intervals_list = [[one_event.start_event, one_event.end_event]]
                interval_time = {"day": one_event.day_start,
                                 "event": one_event.name_event,
                                 "intervals": intervals_list}

                all_booking_this_ev = info_booking.filter(AllBooking.signup_event == one_event.id).all()

                """Поиск интервалов"""
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

                if info_service.duration is not None and info_service.duration != time(hour=0, minute=0, second=0):
                    drop_interval_list = []
                    for one_window in intervals_list:
                        delta_duration = timedelta(hours=info_service.duration.hour,
                                                   minutes=info_service.duration.minute)

                        new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

                        while one_window[1] > new_window.time():
                            drop_interval_list.append([(one_window[0]),
                                                       new_window.time()])
                            one_window[0] = new_window.time()
                            new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

                    intervals_list = drop_interval_list

                interval_time["intervals"] = intervals_list
                answer.append(interval_time)

                #дробь окон
            else:
                "Подготовка апи для одного события"
                for one_day in one_event.many_day:
                    intervals_list = [[one_event.start_event, one_event.end_event]]

                    interval_time = {"day": one_day,
                                     "event": one_event.name_event,
                                     "intervals": intervals_list}

                    all_booking_this_ev = info_booking.filter(db.and_(AllBooking.signup_event == one_event.id,
                                                                      AllBooking.day_booking == one_day)).all()

                    """Поиск интервало"""
                    for one_booking in all_booking_this_ev:
                        for iter_interval in range(len(intervals_list)):
                            if one_booking.time_start >= intervals_list[iter_interval][0] and one_booking.time_end <= \
                                    intervals_list[iter_interval][1]:
                                left_intervals = [intervals_list[iter_interval][0], one_booking.time_start]
                                right_intervals = [one_booking.time_end, intervals_list[iter_interval][1]]

                                intervals_list.pop(iter_interval)
                                intervals_list.extend([left_intervals, right_intervals])
                                break

                    if info_service.duration is not None and info_service.duration != time(hour=0, minute=0, second=0):
                        drop_interval_list = []
                        for one_window in intervals_list:
                            delta_duration = timedelta(hours=info_service.duration.hour,
                                                       minutes=info_service.duration.minute)

                            new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

                            while one_window[1] > new_window.time():
                                drop_interval_list.append([(one_window[0]),
                                                           new_window.time()])
                                one_window[0] = new_window.time()
                                new_window = datetime.combine(date.today(), one_window[0]) + delta_duration

                        intervals_list = drop_interval_list

                    interval_time["intervals"] = intervals_list
                    answer.append(interval_time)


        new_answer = []
        for one_window in answer:
            new_answer.append(json.loads(FrBooking(**one_window).json()))
    except TypeError:
        return None, 404

    return new_answer, 200




