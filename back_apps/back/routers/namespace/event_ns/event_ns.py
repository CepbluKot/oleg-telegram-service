import json
from flask import request, jsonify
from setting_web import db, head_conf, cross_origin
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from pydantic import ValidationError
from flask_restx import Namespace, Resource, fields, reqparse
from datetime import time
from setting_web import token_required
from .validate import ValidateEvent, WindowDataService
from .queries import all_working_date
from ....models.booking_models import EventSetting, ServiceEvent, MyService, EventDay

from .schema import EventSettingSchema

from ..booking_ns.queries import get_indo_calendar
from ..booking_ns.validate import FilterBooking as Filter

event = Namespace('event', 'This-Event_API', validate=True, authorizations=head_conf.auth_setting_swagger)


class TimeFormat(fields.Raw):
    __schema_type__ = "string"
    __schema_format__ = "time"
    def format(self, value):
        return time.strftime(value, "%H:%M")


one_windows_service = event.model("This windows for booking clients", {
    "start_time": TimeFormat(example='13:30'),
    "end_time": TimeFormat(example='16:30')
})


connect_event_service = event.model("Info about connect event and services", {
    "id_service": fields.Integer(example='1'),
    "id_staff": fields.Integer(example='1'),
    "count_service_this_event": fields.List(fields.Nested(one_windows_service))
})


info_event = event.model('Data about one event', {
    "name": fields.String(example='LANCH GOOO'),
    "day_start": fields.Date(example='1971-06-28'),
    "day_end": fields.Date(example='2010-06-04'),
    "day_end_repid": fields.Date(example='2123-09-23'),
    "start_event": TimeFormat(example='13:30'),
    "end_event": TimeFormat(example='17:30'),
    "service_this_day": fields.List(fields.Nested(connect_event_service)),
    "weekday_list": fields.List(fields.Integer, example=[]),
    "status_repid_day": fields.Boolean(example=False)
})

# 1. Редактированик описания
# 2. Редактирование повторений
# 3. Редактирование одного и вынос одного дня


# update_dis = event.model('Обновление описания'{})
#
# update_info_event = event.model("Event update model", {
#     update_description =
#
# })


@event.route('')
class EventApi(Resource):
    @event.doc(security='apikey')
    @cross_origin(origins=["*"], supports_credentials=True)
    @token_required
    def get(self):
        return jsonify(all_working_date())

    @event.doc(security='apikey')
    @event.expect(info_event)
    @token_required
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
        except ValueError:
            return {"message": "not correct input data"}, 401

        if find_new_event:
            object_connect = []
            for one_connect in new_event.service_this_day:

                if one_connect.id_service:
                    correct_data_window = {}
                    for one_window in one_connect.count_service_this_event:
                        correct_data_window[str(one_window.start_time)] = json.loads(WindowDataService(start_time=one_window.start_time,
                                                                                            end_time=one_window.start_time,
                                                                                            status_booking=False).json())

                    print(correct_data_window)
                    object_connect.append(ServiceEvent(event_id=find_new_event.id,
                                                        service_id=one_connect.id_service,
                                                        windows_service=correct_data_window))
                else:
                    return {"message": "dont find service"}, 401

            db.session.add_all(object_connect)

            calendar_date = Filter()
            calendar_date.this_date_filter = find_new_event.day_start_g
            return jsonify(get_indo_calendar(calendar_date)), 200
        else:
            return {"message": "DONT ADD EVENT"}, 404

    @event.doc(params={'event_set_id': 'id'})
    def delete(self):
        event_url_parse = reqparse.RequestParser()
        event_url_parse.add_argument("event_set_id", type=int)

        try:
            id_event = event_url_parse.parse_args()['event_set_id']
        except KeyError:
            return {"message": "not correct url"}, 404

        data_event = EventSetting.find_by_id(id_event)

        if data_event:
            data_event.delete_from_db()
            return {"message": "deletion successful"}, 200
        else:
            return {"message": "not correct input data"}, 401


# @event.route('/update/')
# @event.expect(update_info_event)
# class EventApiUpdate(Resource):
#     @event.doc(params={'event_set_id': {'description': 'id', 'type': 'int'}})
#     @event.doc(params={'new_ev': {'description': 'status create new event', 'type': 'str', 'example': 'y or n'}})
#     def put(self):
#         event_url_parse = reqparse.RequestParser()
#         event_url_parse.add_argument('event_set_id', type=int)
#         event_url_parse.add_argument('new_ev', type=str)
#
#         event_set_id, new_ev = event_url_parse.parse_args().values()
#
#
#
#         print(event_set_id, new_ev)


@event.route('/event_day/')
class EventDayApi(Resource):
    @event.doc(params={'event_day_id': {'description': 'id конкретного дня события', 'type': 'int'}})
    def delete(self):
        event_url_parse = reqparse.RequestParser()
        event_url_parse.add_argument('event_day_id', type=int)

        event_id_service = event_url_parse.parse_args()["event_day_id"]
        print(event_id_service)

        try:
            info_event_day = EventDay.find_by_event_day_id(event_day_id_=event_id_service)
            if info_event_day is not None:
                 info_event_day.delete_from_db()
                 return EventDay.find_by_event_day_id(event_day_id_=event_id_service), 200
            else:
                return {"message": "not find this event_day"}, 404
        except:
            return {"message": "not correct input data"}, 401