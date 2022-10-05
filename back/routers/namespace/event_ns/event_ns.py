import json
from flask import request, jsonify
from setting_web import flask_app, db, head_conf, cross_origin
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from pydantic import ValidationError
from flask_restplus import Namespace, Resource, fields
from datetime import time
from setting_web import token_required
from .validate import ValidateEvent, FilterEvent as Filter, WindowDataService
from .queries import get_filter_work_day, find_boundaries_week, all_working_date
from .schema import EventSettingSchema
from back.models.booking_models import EventSetting, ServiceEvent, MyService


event = Namespace('event', 'This-Event_API', authorizations=head_conf.auth_setting_swagger)


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
    "weekday_list": fields.List(fields.Integer, example=[]),
    "status_repid_day": fields.Boolean(example=False),
    "day_end_repid": fields.Date(example='2123-09-23')
})


update_info_event = event.model("Event update model", {
    "name_field_change_date": fields.List(fields.String(), example=[]),
    "data_service": fields.Nested(one_windows_service)
})


@event.route('')
class EventApi(Resource):
    @event.doc(security='apikey')
    @cross_origin(origins=["*"], supports_credentials=True)
    @token_required
    def get(self):
        return all_working_date()

    @event.expect(info_event)
    @cross_origin(origins=["*"], supports_credentials=True)
    def post(self):
        try:
            new_event = ValidateEvent(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404
        try:
            find_new_event = EventSetting(day_start_g=new_event.day_start,
                            day_end_g=new_event.day_end,
                            event_time_start=new_event.start_event,
                            event_time_end=new_event.end_event,
                            name_event=new_event.name,
                            weekdays=new_event.weekday_list,
                            status_repid_day=new_event.status_repid_day,
                            day_end_rapid=new_event.day_end_repid
                        )

        except PendingRollbackError:
            return {"message": "this event alredy exist"}, 401
        except IntegrityError:
            return {"message": "this event alredy exist"}, 401

        if find_new_event:
            object_connect = []
            for one_connect in new_event.service_this_day:
                find_services = MyService.find_by_name(one_connect.name_service)

                if find_services:
                    correct_data_window = {}
                    for one_window in one_connect.count_service_this_event:
                        correct_data_window[str(one_window.start_time)] = json.loads(WindowDataService(start_time=one_window.start_time,
                                                                                            end_time=one_window.start_time,
                                                                                            status_booking=False).json())

                    print(correct_data_window)
                    object_connect.append(ServiceEvent(event_id=find_new_event.id,
                                                        service_id=find_services.id,
                                                        windows_service=correct_data_window))
                else:
                    return {"message": "dont find service"}, 401

            db.session.add_all(object_connect)

            return {"message": "amazing add event"}, 200
        else:
            return {"message": "DONT ADD EVENT"}, 404

    @event.expect(update_info_event)
    def put(self):
        pass


    def delete(self):
        pass
