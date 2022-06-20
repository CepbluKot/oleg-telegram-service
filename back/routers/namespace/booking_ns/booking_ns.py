from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from queries.queries_booking import get_all_booking, get_filter_booking

from models.all_models import AllBooking

from .dataclass_booking import FilterBooking as Filter

booking = Namespace('booking', 'This-booking_API')

booking_inset = booking.model('Booking', {
    "time_start": fields.DateTime(description='start_booking', required=True),
    "time_end": fields.DateTime(description='end_booking', required=True),
    "event_id": fields.Integer(description='fk event table', required=True),
    "service_id": fields.Integer(description='fk service table', required=True),
    "staff_id": fields.Integer(description='fk staff table', required=True),
    "client_id": fields.Integer(description='fk client table', required=True),
})


@booking.route('')
class Booking(Resource):
    def get(self):
        return jsonify(get_all_booking())

    @booking.expect(booking_inset)
    def post(self):
        new_booking = AllBooking(**request.get_json())
        new_booking.save_to_db()

        return jsonify(get_all_booking())


booking_filter = booking.model('Booking', {
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
        res_data = get_filter_booking(Filter)







