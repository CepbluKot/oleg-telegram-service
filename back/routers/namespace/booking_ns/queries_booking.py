from queries.queries_workig_date import find_boundaries_week
from models.all_models import *

from .dataclass_booking import FilterBooking as Filter
from .booking_schema import InfoBookingSchema

from pprint import pprint

def _base_query():
    """Базовый запрос"""
    booking = AllBooking.query
    return booking


def get_all_booking():
    """Все записи"""
    all_booking = _base_query()
    api_all_booking_schema = InfoBookingSchema(many=True)

    return api_all_booking_schema.dump(all_booking)


def get_filter_booking(new_filter: Filter):
    all_booking_service = _base_query()

    """Filter about people"""
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
        between_date = Event.day.between(new_filter.date_start_filter, new_filter.date_end_filter)
        all_booking_service = all_booking_service.filter(between_date)

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
        pprint("error: fun in get_indo_calendar")
        return None

    return get_filter_booking(cor_date)

