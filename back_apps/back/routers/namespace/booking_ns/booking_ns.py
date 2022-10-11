from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse
from datetime import time, datetime
from pydantic import ValidationError

from sqlalchemy.exc import IntegrityError
from .queries import get_indo_calendar, get_all_event, find_freedom_booking
from ....models.booking_models import AllBooking
from .validate import FilterBooking as Filter, BookingValidate

from setting_web import cross_origin, token_required

booking = Namespace('booking', 'This-booking_API')

class TimeFormat(fields.Raw):
    __schema_type__ = "string"
    __schema_format__ = "time"
    def format(self, value):
        return time.strftime(value, "%H:%M")


booking_inset = booking.model('BookingInsert', {
    "time_start": TimeFormat(required=True, description='Time in HH:MM', example='13:37'),
    "time_end": TimeFormat(description='Time in HH:MM', example='02:28'),
    "event_setting_id": fields.Integer(description='fk event table', required=True),
    "day_start": fields.Date(example='1971-06-28'),
    "day_end": fields.Date(example='1971-06-28'),
    "service_id": fields.Integer(description='fk service table', required=True),
    "staff_id": fields.Integer(description='fk staff table', required=True),
    "client_id": fields.Integer(description='fk client table', required=True)
})


@cross_origin(origins=["*"], supports_credentials=True)
@booking.route('')
class Booking(Resource):
    @booking.doc(security='apikey')
    @token_required
    def get(self):
        return get_all_event(), 200

    @booking.doc(security='apikey')
    @token_required
    @booking.expect(booking_inset)
    def post(self):
        try:
            obj_booking = BookingValidate(**request.get_json())
        except ValidationError as e:
            return {'message': e.json()}, 401

        try:
            new_booking_start = AllBooking(event_setting_id=obj_booking.event_setting_id,
                                           day=obj_booking.day_start,
                                           service_id=obj_booking.service_id,
                                           time_start=obj_booking.time_start,
                                           time_end=obj_booking.time_end,
                                           client_id=obj_booking.client_id)

            if obj_booking.day_end != obj_booking.day_start:
                 new_booking_end = AllBooking(event_setting_id=obj_booking.event_setting_id,
                                              day=obj_booking.day_end,
                                              service_id=obj_booking.service_id,
                                              time_start=obj_booking.time_start,
                                              time_end=obj_booking.time_end,
                                              client_id=obj_booking.client_id)
        except IntegrityError:
            return {'message': "not correct data"}, 401

        if new_booking_start is None: #потестить
            return {'message': "not correct data"}, 401
        return {'message': "add new booking"}, 200

    @booking.doc(security='apikey')
    @token_required
    @booking.doc(params={'id_bookings': 'id'})
    def delete(self):
        parser_booking = reqparse.RequestParser()
        parser_booking.add_argument("id_bookings", type=int)

        args = parser_booking.parse_args()

        find_book = AllBooking.find_booking_by_event_id(int(args['id_bookings']))

        if find_book:
            find_book.delete_from_db()
            return {"message": "delete good"}, 200
        else:
            return {"message": "date not correct"}, 404


booking_filter = booking.model('BookingFilter', {
    "this_date_filter": fields.Date(description='all bookings for this day', required=True),
    "date_start_filter": fields.Date(description='date beginning of the range', required=True),
    "date_day_filter": fields.Date(description='data end of range', required=True),
    "service_filter": fields.List(fields.String()),
    "time_start_filter": fields.DateTime(description='need testing', required=True),
    "time_end_filter": fields.DateTime(description='need testing', required=True),
})


# @booking.route('/filter')
# class FilterBooking(Resource):
#
#     @booking.expect(booking_filter)
#     def post(self):
#         add_filter = Filter(**request.get_json())
#         res_data = get_filter_booking(add_filter)

@booking.route('/calendar')
class CalendarBooking(Resource):
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @booking.doc(security='apikey')
    @token_required
    @booking.doc(params={'cal_date': 'date format 2022-05-27'})
    def get(self):
        parser_booking = reqparse.RequestParser()
        parser_booking.add_argument("cal_date", type=str)

        args = parser_booking.parse_args()

        try:
            cal_date = datetime.strptime(args["cal_date"], '%Y-%m-%d').date()
        except ValueError:
            return {"Error": "not correct data-format in query"}, 404

        calendar_date = Filter()
        calendar_date.this_date_filter = cal_date
        return jsonify(get_indo_calendar(calendar_date)), 200


freedom_booking = booking.model('FreedomBooking', {
    "name_service": fields.String(description='search for a free reservation by event name')
})


@booking.route('/search')
class BookingSearch(Resource):
    @booking.expect(freedom_booking)
    def post(self):
        name_service = request.get_json()['name_service']
        return find_freedom_booking(name_service)