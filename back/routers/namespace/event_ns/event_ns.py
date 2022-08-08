from flask import request
from setting_web import cross_origin
from flask_restplus import Namespace, Resource, fields

from .queries_event import get_filter_work_day, find_boundaries_week, all_working_date
from models.all_models import Event


event = Namespace('event', 'This-Event_API')


@event.route('')
class Booking(Resource):
    @cross_origin(origins=["*"], supports_credentials=True)
    def post(self):
        new_service = request.get_json()
        print(new_service)
        return "ZALUOPA"
