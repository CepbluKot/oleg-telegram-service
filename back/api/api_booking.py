from setting_web import flask_app, db, ma
from datetime import date, datetime, time
from models.booking_date_connecta import AllBooking
from models.days_coonecta import Days
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.all_users_this_connecta import CompanyUsers

import api.api_authentication as auth
from api.api_workig_date import find_boundaries_week

class InfoBookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'time_start', 'time_end', 'name_client', 'tg_id', 'phone_num', 'name_service', 'day')


def _base_query():
    """Базовый запрос"""
    booking = db.session.query(AllBooking.id, AllBooking.time_start, AllBooking.time_end, CompanyUsers.name_client, CompanyUsers.tg_id,
                               CompanyUsers.phone_num, MyStaff.name_staff, MyService.name_service, Days.day)
    booking = booking.join(CompanyUsers)
    booking = booking.join(Days)
    booking = booking.join(MyService)
    booking = booking.join(MyStaff)

    return booking


def get_all_booking():
    """Все записи"""
    all_booking = _base_query()
    api_all_booking_schema = InfoBookingSchema(many=True)

    return api_all_booking_schema.dump(all_booking)


def get_filter_booking(my_service=None, my_date=None, date_start=None, date_end=None, g_time_start=None, g_time_end=None):
    all_booking_service = _base_query()

    if my_service is not None:
        all_booking_service = all_booking_service.filter(MyService.name_service == my_service)

    if my_date is not None:
        this_date = datetime.strptime(my_date, '%Y-%m-%d').date()
        all_booking_service = all_booking_service.filter(db.and_(MyService.name_service == my_service, Days.day == this_date))

    if (date_start is not None) and (date_end is not None) and (my_date is None):
        try:
            cor_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
            cor_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
        except ValueError:
            return {"Error": "not correct query"}
        all_booking_service = all_booking_service.filter(Days.day.between(cor_date_start, cor_date_end))

    if g_time_start is not None and g_time_end is not None:
        time_start = time(hour=g_time_start)
        time_end = time(hour=g_time_end)
        all_booking_service = all_booking_service.filter(AllBooking.time_start.between(time_start, time_end))

    all_booking_service = all_booking_service.order_by(db.desc(AllBooking.time_start))
    api_all_booking_schema = InfoBookingSchema(many=True)
    return api_all_booking_schema.dump(all_booking_service)


def get_indo_calendar(select_day=None):
    if select_day is not None:
        try:
            cor_date = datetime.strptime(select_day, '%Y-%m-%d').date()
        except ValueError:
            return {"Error": "not correct query"}
    else:
        return {"Error": "not correct query"}

    start_end_weeks = find_boundaries_week(cor_date)
    return get_filter_booking(date_start=start_end_weeks[0], date_end=start_end_weeks[-1])

