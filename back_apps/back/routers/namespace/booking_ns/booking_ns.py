from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse
from datetime import time, datetime
from pydantic import ValidationError

from sqlalchemy.exc import IntegrityError
from .queries import get_all_event, find_freedom_booking
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
    "booking_time_start": TimeFormat(required=True, description='Time in HH:MM', example='13:37'),
    "booking_time_end": TimeFormat(description='Time in HH:MM', example='02:28'),
    "event_day_id": fields.Integer(description='fk event table', required=True),
    "booking_day_start": fields.Date(example='1971-06-28'),
    "booking_day_end": fields.Date(example='1971-06-28'),
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
                                           event_day_id=obj_booking.event_day_id,
                                           service_id=obj_booking.service_id,
                                           time_start=obj_booking.time_start,
                                           time_end=obj_booking.time_end,
                                           client_id=obj_booking.client_id)

            if obj_booking.day_end != obj_booking.day_start:
                 new_booking_end = AllBooking(event_setting_id=obj_booking.event_setting_id,
                                              day=obj_booking.day_end,
                                              event_day_id=obj_booking.event_day_id,
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


freedom_booking = booking.model('FreedomBooking', {
    "name_service": fields.String(description='search for a free reservation by event name')
})


@booking.route('/search')
class BookingSearch(Resource):
    @booking.expect(freedom_booking)
    def post(self):
        name_service = request.get_json()['name_service']
        return find_freedom_booking(name_service)