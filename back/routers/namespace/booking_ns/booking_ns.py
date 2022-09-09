from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from datetime import time, date, datetime

from .queries import get_all_booking, get_filter_booking, get_indo_calendar, find_freedom_booking, get_all_event
from models.all_models import AllBooking
from .validate import FilterBooking as Filter


class TimeFormat(fields.Raw):
    def format(self, value):
        return time.strftime(value, "%H:%M")


booking = Namespace('booking', 'This-booking_API')

booking_inset = booking.model('BookingInsert', {
    "time_start": TimeFormat(required=True, description='Time in HH:MM', default='HH:MM'),
    "time_end": TimeFormat(required=True, description='Time in HH:MM', default='HH:MM'),
    "event_id": fields.Integer(description='fk event table', required=True),
    "service_id": fields.Integer(description='fk service table', required=True),
    "staff_id": fields.Integer(description='fk staff table', required=True),
    "client_id": fields.Integer(description='fk client table', required=True),
})


@booking.route('')
class Booking(Resource):
    def get(self):
        return jsonify(get_all_event())

    @booking.expect(booking_inset)
    def post(self):
        new_booking = AllBooking(**request.get_json())
        new_booking.save_to_db()

        return jsonify(get_all_booking())


booking_filter = booking.model('BookingFilter', {
    "this_date_filter": fields.Date(description='all bookings for this day', required=True),
    "date_start_filter": fields.Date(description='date beginning of the range', required=True),
    "date_day_filter": fields.Date(description='data end of range', required=True),
    "service_filter": fields.List(fields.String()),
    "time_start_filter": fields.DateTime(description='need testing', required=True),
    "time_end_filter": fields.DateTime(description='need testing', required=True),
})


@booking.route('/filter')
class FilterBooking(Resource):

    @booking.expect(booking_filter)
    def post(self):
        add_filter = Filter(**request.get_json())
        res_data = get_filter_booking(add_filter)


@booking.route('/calendar/string:<cal_date>')
@booking.doc(params={'cal_date': 'date format 2022-05-27'})
class CalendarBooking(Resource):
    def get(self, cal_date: str):
        try:
            cal_date = datetime.strptime(cal_date, '%Y-%m-%d').date()
        except ValueError:
            return {"Error": "not correct data-format in query"}

        calendar_date = Filter()
        calendar_date.this_date_filter = cal_date
        return get_indo_calendar(calendar_date)


freedom_booking = booking.model('FreedomBooking', {
    "name_service": fields.String(description='search for a free reservation by event name')
})


@booking.route('/search')
class BookingSearch(Resource):
    @booking.expect(freedom_booking)
    def post(self):
        name_service = request.get_json()['name_service']
        return find_freedom_booking(name_service)