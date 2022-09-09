from models.all_models import *
from routers.namespace.event_ns.queries import find_boundaries_week
from operator import ge

from .validate import FilterBooking as Filter, FreedomBooking as FrBooking
from .schema import InfoBookingSchema, EventSchema

from datetime import datetime

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
        all_booking_service = all_booking_service.filter(MyService.name_service.in_(new_filter.date_start_filter))

    if (new_filter.date_start_filter is not None) and (new_filter.date_end_filter is not None) \
            and (new_filter.this_date_filter is None):
        between_date = Event.day_start.between(new_filter.date_start_filter, new_filter.date_end_filter)
        single_date = all_booking_service.filter(between_date)

        many_date = all_booking_service.filter(Event.many_day is not None)
        many_date = many_date.filter(Event.many_day.any(new_filter.date_start_filter, operator=ge))

        all_booking_service = many_date

    if new_filter.time_start_filter is not None and new_filter.time_end_filter is not None:
        between_time = AllBooking.time_start.between(new_filter.time_start_filter, new_filter.time_end_filter)
        all_booking_service = all_booking_service.filter(between_time)

    all_booking_service = all_booking_service.order_by(db.desc(AllBooking.time_start))
    api_all_booking_schema = InfoBookingSchema(many=True)

    return api_all_booking_schema.dump(all_booking_service)


def get_indo_calendar(cor_date: Filter):
    """Calendar Booking"""
    try:
        start_end_weeks = find_boundaries_week(cor_date.this_date_filter)
        cor_date.date_start_filter = start_end_weeks[0]
        cor_date.date_end_filter = start_end_weeks[-1]
        cor_date.this_date_filter = None
    except:
        print("error: fun in get_indo_calendar")
        return None
    print(cor_date.json())

    return get_filter_booking(cor_date)


def find_freedom_booking(name_service):
    con_ser_event = ServiceEvent.event_search_by_service(name_service)
    info_service = MyService.query.filter(MyService.name_service == name_service).first()

    all_event_id = []
    for one_q in con_ser_event:
        all_event_id.append(one_q.event_id)

    now_date = datetime.now()
    info_events = Event.query.filter(db.and_(Event.id.in_(all_event_id),
                                       Event.day_end >= date(year=now_date.year, month=now_date.month, day=now_date.day))).all()

    info_booking = AllBooking.find_booking_by_event_id(all_event_id)

    answer = []
    for one_event in info_events:
        print(one_event.weekdays)
        if one_event.weekdays is None or len(one_event.weekdays) == 0:
            intervals_list = [[one_event.start_event, one_event.end_event]]
            interval_time = {"day": one_event.day_start,
                             "event": one_event.name_event,
                             "intervals": intervals_list}

            all_booking_this_ev = info_booking.filter(AllBooking.signup_event == one_event.id).all()

            """Посмотреть как убрать повтор"""
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

            interval_time["intervals"] = intervals_list
            answer.append(interval_time)
        else:
            for one_day in one_event.many_day:
                intervals_list = [[one_event.start_event, one_event.end_event - info_service.duration]]
                interval_time = {"day": one_day,
                                 "event": one_event.name_event,
                                 "intervals": intervals_list}

                all_booking_this_ev = info_booking.filter(db.and_(AllBooking.signup_event == one_event.id,
                                                                  AllBooking.day == one_day)).all()
                """Посмотреть как убрать повтор"""
                for one_booking in all_booking_this_ev:
                    for iter_interval in range(len(intervals_list)):
                        if one_booking.time_start >= intervals_list[iter_interval][0] and one_booking.time_end <= \
                                intervals_list[iter_interval][1]:
                            left_intervals = [intervals_list[iter_interval][0], one_booking.time_start]
                            right_intervals = [one_booking.time_end, intervals_list[iter_interval][1]]

                            intervals_list.pop(iter_interval)
                            intervals_list.extend([left_intervals, right_intervals])
                            break

                interval_time["intervals"] = intervals_list
                answer.append(interval_time)

    new_answer = []
    for one_window in answer:
        new_answer.append(FrBooking(**one_window).json())

    return new_answer




