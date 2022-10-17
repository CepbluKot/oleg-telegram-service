from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse
from pydantic import ValidationError
from datetime import time
from sqlalchemy.exc import IntegrityError


from setting_web import cross_origin, token_required
from ....models.booking_models import MyService, ServiceStaffConnect
from .queries import all_service, get_filter_services
from .validate import ValidateService as ValidateService
from .validate import FilterServicesStaff as Filter
from .validate import AllConnectServiceStaff as ConnectStaffService


class TimeFormat(fields.Raw):
    __schema_type__ = "string"
    __schema_format__ = "time"
    def format(self, value):
        return time.strftime(value, "%H:%M")


service = Namespace('service')


add_service = service.model('service model', {
     "name_service": fields.String(description='new_service', required=True, example='New Service'),
     "price": fields.Float(example=133.7),
    "duration": TimeFormat(example="HH:MM:SS"),
    "max_booking": fields.Integer(example=1337)
})

list_add_service = service.model('list adder model', {
    "all_adder": fields.List(fields.Nested(add_service, description='all adder service'))
})

answer_response = service.model('ANSWER EXAMPLE ERROR', {
    "message": fields.String()
})


@service.route('')
class AllService(Resource):
    def get(self):
        return all_service()

    @service.expect(list_add_service)
    @service.response(400, 'Bad Request', model=answer_response)
    @service.response(200, 'Success', model=answer_response)
    @cross_origin(origins=["*"], supports_credentials=True)
    def post(self):
        add_services = request.get_json()['all_adder']

        try:
            for one_service in add_services:
                try:
                    ValidateService(**one_service)
                except ValidationError as e:
                    print(e)
                    return jsonify({'message': e.json()}), 400
                except TypeError:
                    return jsonify({'message': "Incorrect data entry"}), 400

                new_service = MyService(**one_service)
                new_service.save_to_db()
        except IndexError :
            return jsonify({'message': 'dont add new service'}), 400
        except IntegrityError:
            return jsonify({'message': 'dont add new service'}), 400

        return jsonify({'message': 'successful addition'}), 200


@service.route('/one_service')
@service.doc(params={'service_name': 'name_service'})
class OneService(Resource):

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @service.doc(security='apikey')
    @token_required
    def get(self, service_name):
        service_url_parser = reqparse.RequestParser()
        service_url_parser.add_argument("service_name", type=str)

        service_name = service_url_parser.parse_args()["service_name"]

        if service_name:
            return get_filter_services(Filter(name_services=[service_name])), 200
        else:
            return {"message": "not input"}, 400

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @service.doc(security='apikey')
    @token_required
    @service.expect(add_service)
    def put(self, service_name):
        find_ser = MyService.find_by_name(service_name)

        if find_ser:
            try:
                update_ser = ValidateService(**request.get_json())
            except ValidationError as e:
                print(e)
                return {'message': e.json()}, 404

            find_ser.name_service = update_ser.name_service
            find_ser.price_service = update_ser.price
            find_ser.update_from_db()
        else:
            return {'message': "Incorrect data entry"}, 404

        return get_filter_services(Filter(name_services=[service_name])), 200

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @service.doc(security='apikey')
    @token_required
    def delete(self, service_name=None):
        if service_name is not None:
            find_service = MyService.find_by_name(service_name)
            if find_service:

                find_connect = ServiceStaffConnect.find_name(service_name)
                for one_connect in find_connect:
                    one_connect.delete_from_db()

                find_service.delete_from_db()
                return {'message': "SERVICE DELETE"}, 200
            return {'ERROR': 'SERVICE NOT FIND'}, 404

        return {'ERROR': 'SERVICE TYPE NONE'}, 404


service_filter = service.model('AddService', {
     "name_services": fields.List(fields.String(description='filter services', required=True)),
     "name_staff": fields.List(fields.String(description='filter staff', required=True))
})


@service.route('/filter')
class FilterServices(Resource):
    @service.expect(service_filter)
    def post(self):
        print(request.get_json())
        add_filter = Filter(**request.get_json())
        res_data = get_filter_services(add_filter)
        return res_data


service_staff = service.model('AddServiceStaffConnect', {
     "name_service": fields.String(description='filter services', required=True),
     "name_staff": fields.String(description='filter staff', required=True)
})

list_ser_sf = service.model("ListServiceStaff", {
    "all_connect": fields.List(fields.Nested(service_staff, allow_null=True),
                               description="all connect staff and service")
})


@service.route('/connect_service_staff')
class StaffServiceConnect(Resource):

    @service.expect(list_ser_sf)
    def post(self):
        all_data_connect = ConnectStaffService(**request.get_json())
        all_service_name = []

        for one_connect in all_data_connect.all_connect:
            ServiceStaffConnect(name_service=one_connect.name_service, name_staff=one_connect.name_staff)
            all_service_name.append(one_connect.name_service)

        return get_filter_services(Filter(name_services=all_service_name))

    @service.expect(list_ser_sf)
    def delete(self):
        all_data_connect = ConnectStaffService(**request.get_json())
        all_delete = []
        not_delete = []

        for one_connect in all_data_connect.all_connect:
            find_c = ServiceStaffConnect.find_connect(name_service=one_connect.name_service, name_staff=one_connect.name_staff)
            if find_c:
                find_c.delete_from_db()
                all_delete.append([one_connect.name_service, one_connect.name_staff])
            else:
                not_delete.append([one_connect.name_service, one_connect.name_staff])

        return {"delete": all_delete, "not_delete": not_delete}
