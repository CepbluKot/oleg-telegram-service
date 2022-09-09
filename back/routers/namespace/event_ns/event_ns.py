from flask import request
from setting_web import cross_origin
from pydantic import ValidationError
from flask_restplus import Namespace, Resource, fields
from datetime import time

from .validate import ValidateEvent, FilterEvent as Filter, WindowDataService
from .queries import get_filter_work_day, find_boundaries_week, all_working_date
from .schema import EventSchema
from models.all_models import Event, ServiceEvent, MyService


event = Namespace('event', 'This-Event_API')


class TimeFormat(fields.Raw):
    def format(self, value):
        return time.strftime(value, "%H:%M")


one_windows_service = event.model("This windows for booking clients", {
    "start_time": TimeFormat(example='13:30'),
    "end_time": TimeFormat(example='16:30')
})


connect_event_service = event.model("Info about connect event and services", {
    "name_service": fields.String(example='chistka'),
    "name_staff": fields.String(example='Kirill'),
    "count_service_this_event": fields.List(fields.Nested(one_windows_service))
})


info_event = event.model('Data about one event', {
    "name": fields.String(example='LANCH GOOO'),
    "day_start": fields.Date(example='1971-06-28'),
    "day_end": fields.Date(example='2010-06-04'),
    "start_event": TimeFormat(example='13:30'),
    "end_event": TimeFormat(example='17:30'),
    "service_this_day": fields.List(fields.Nested(connect_event_service)),
    "weekday_list": fields.List(fields.Integer)
})


@event.route('')
class Booking(Resource):
    def get(self):
        return all_working_date()

    @cross_origin(origins=["*"], supports_credentials=True)
    @event.expect(info_event)
    def post(self):
        try:
            new_event = ValidateEvent(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        Event(day_start=new_event.day_start,
              day_end=new_event.day_end,
              start_event=new_event.start_event,
              end_event=new_event.end_event,
              name=new_event.name,
              weekdays_list=new_event.weekday_list
              )

        find_new_event = Event.find_by_all_parameters(name_=new_event.name,
                                                      day_start_=new_event.day_start,
                                                      day_end_=new_event.day_end,
                                                      time_start_=new_event.start_event,
                                                      time_end_=new_event.end_event)


        if find_new_event:
            object_connect = []
            for one_connect in new_event.service_this_day:
                find_services = MyService.find_by_name(one_connect.name_service)

                if find_services:
                    correct_data_window = {}
                    for one_window in one_connect.count_service_this_event:
                        correct_data_window[str(one_window.start_time)] = WindowDataService(start_time=one_window.start_time,
                                                                                            end_time=one_window.start_time,
                                                                                            status_booking=False).json()

                    print(correct_data_window)
                    object_connect.append(ServiceEvent(event_id=find_new_event.id,
                                                        service_id=find_services.id,
                                                        windows_service=correct_data_window))
                else:
                    return {"message": "DONT ADD CONNECT"}, 404

            for one_connect in object_connect:
                one_connect.save_to_db()

            api_schema_event = EventSchema()
            return api_schema_event.dump(find_new_event), 200
        else:
            return {"message": "DONT ADD EVENT"}, 404
