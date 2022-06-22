from flask import request
from flask_restplus import Namespace, Resource, fields

from .queries_event import get_filter_work_day, find_boundaries_week, all_working_date
from models.all_models import Event


event = Namespace('event', 'This-Event_API')


@event.route('')
class Booking(Resource):
    def get(self):
        return all_working_date()
