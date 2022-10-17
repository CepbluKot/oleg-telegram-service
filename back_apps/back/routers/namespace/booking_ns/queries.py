from ....models.booking_models import AllBooking, EventDay, MyService, ServiceEvent, EventSetting
from setting_web import db
from sqlalchemy import between
from typing import List

from .validate import FilterBooking as Filter, FreedomBooking as FrBooking
from .schema import InfoBookingSchema, EventDaySchema

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
    # query_event = EventDay.query.filter(EventDay.day_start >= date(year=now_date.year, month=now_date.month, day=now_date.day))
    query_event = EventDay.query

    api_all_event = EventDaySchema(many=True)
    return api_all_event.dump(query_event)


def find_intervals(intervals_list, all_booking_this_ev: List[AllBooking], traced_day: date):
    for one_booking in all_booking_this_ev:  #проходит по всем броням
        if one_booking.booking_day_start <= traced_day <= one_booking.booking_day_end:

            for iter_interval in range(len(intervals_list)): #находим интервал в котором находится запись
                if one_booking.booking_time_start >= intervals_list[iter_interval][0] \
                        or one_booking.booking_time_end <= intervals_list[iter_interval][1]:

                    if one_booking.booking_day_end == traced_day and one_booking.booking_day_start == traced_day:
                        left_intervals = [intervals_list[iter_interval][0], one_booking.booking_time_start]
                        right_intervals = [one_booking.booking_time_end, intervals_list[iter_interval][1]]

                    elif one_booking.booking_day_end == traced_day and one_booking.booking_day_start < traced_day:
                        left_intervals = [one_booking.booking_time_end, intervals_list[iter_interval][1]]
                        right_intervals = []

                    elif one_booking.booking_day_start == traced_day and one_booking.booking_day_end > traced_day:
                        right_intervals = [intervals_list[iter_interval][0], one_booking.booking_time_start] #генирируем новый интервал
                        left_intervals = []

                    intervals_list.pop(iter_interval)

                    if len(left_intervals) != 0 and left_intervals[0] != left_intervals[1]:
                        intervals_list.append(left_intervals)
                    if len(right_intervals) != 0 and right_intervals[0] != right_intervals[1]:
                        intervals_list.append(right_intervals)
                    break

    return intervals_list


def fraction_window(intervals_list, dur_service):
    if dur_service is not None and dur_service != time(hour=0, minute=0, second=0):
        drop_interval_list = []
        for one_window in intervals_list:
            delta_duration = timedelta(hours=dur_service.hour,
                                       minutes=dur_service.minute)

            new_window = datetime.combine(date(year=1, month=1, day=1), one_window[0]) + delta_duration

            while one_window[1] > new_window.time():
                print(new_window.time(), one_window[1])
                drop_interval_list.append([one_window[0], new_window.time()])
                one_window[0] = new_window.time()

                new_window = datetime.combine(date(year=1, month=1, day=1), new_window.time()) + delta_duration

                if one_window[0] > new_window.time():
                    break

        intervals_list = drop_interval_list

    return intervals_list


def start_intervals_day(event_day: EventDay, tracer_day: date = None):
    if event_day.day_start == event_day.day_end or tracer_day is None: #если событие однодневное
        return [[event_day.event_time_start, event_day.event_time_end]]

    elif tracer_day is not None:
        if event_day.day_start < tracer_day < event_day.day_end:
            return [[time(hour=0), time(hour=23, minute=59)]]
        elif event_day.day_start == tracer_day:
            return [[event_day.event_time_start, time(hour=23, minute=59)]]
        elif event_day.day_end == tracer_day:
            return [[time(hour=0), event_day.event_time_end]]

    else:
        raise ValueError


def find_freedom_booking(name_service):
    con_ser_event = ServiceEvent.event_day_search_by_service(name_service)

    answer = []
    now_date = datetime.now()
    this_day = date(year=now_date.year, month=now_date.month, day=now_date.day)
    try:
        for days_query in con_ser_event:
            info_event_day: EventDay = days_query.EventDay
            dur_service = days_query.duration

            all_booking_this_ev = AllBooking.find_booking_by_event_id(info_event_day.id)
            if all_booking_this_ev:
                all_booking_this_ev = all_booking_this_ev.all()  #проверка на пустоту запроса
            else:
                all_booking_this_ev = []


            if info_event_day.day_start < info_event_day.day_end: #если событие разделено на несколько дней
                start_iteration_day = info_event_day.day_start
                # if this_day > info_event_day.day_start: #корректирует дату, событие может уже начаться настоящий момент времени
                #     start_iteration_day = this_day

                delta_days = info_event_day.day_end - start_iteration_day
                for iter_day in range(delta_days.days + 1):
                    intervals_list = start_intervals_day(info_event_day, tracer_day=start_iteration_day + timedelta(days=iter_day))

                    interval_json = {"day": start_iteration_day + timedelta(days=iter_day),
                                     "id_event": info_event_day.id,
                                     "name_event": days_query.name_event,
                                     "intervals": intervals_list}

                    intervals_list = find_intervals(intervals_list, all_booking_this_ev, start_iteration_day + timedelta(days=iter_day))
                    intervals_list = fraction_window(intervals_list, dur_service)

                    interval_json["intervals"] = intervals_list #заполняем отсувствующие интервалы
                    answer.append(interval_json)

            else:
                intervals_list = start_intervals_day(info_event_day)

                interval_json = {"day": info_event_day.day_start,
                                 "id_event": info_event_day.id,
                                 "name_event": days_query.name_event,
                                 "intervals": intervals_list}

                intervals_list = find_intervals(intervals_list, all_booking_this_ev, info_event_day.day_start)
                intervals_list = fraction_window(intervals_list, dur_service)

                interval_json["intervals"] = intervals_list
                answer.append(interval_json)

        new_answer = []
        for one_window in answer:
            new_answer.append(json.loads(FrBooking(**one_window).json()))
    except TypeError:
        return {"message": "not find this service"}, 404

    return new_answer, 200




