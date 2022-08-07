from flask import request
from flask_restplus import Namespace, Resource, fields
from pydantic import ValidationError

from models.all_models import MyService, ServiceStaffConnect
from .queries import all_service, get_filter_services
from .validate import ValidateService as ValidateService
from .validate import FilterServicesStaff as Filter
from .validate import AllConnectServiceStaff as ConnectStaffService

service = Namespace('service')


add_service = service.model('add service model', {
     "name_service": fields.String(description='new_service', required=True),
     "price": fields.Float()
})

list_add_service = service.model('list adder model', {
    "all_adder": fields.List(fields.Nested(add_service, description='all adder service'))
})


@service.route('')
class AllService(Resource):
    def get(self):
        return all_service()

    @service.expect(list_add_service)
    def post(self):
        add_services = request.get_json()['all_adder']

        try:
            for one_service in add_services:
                try:
                    ValidateService(**one_service)
                except ValidationError as e:
                    print(e)
                    return {'message': e.json()}, 404
                except TypeError:
                    return {'message': "Incorrect data entry"}, 404

                new_service = MyService(**one_service)
                new_service.save_to_db()
        except IndexError:
            return {'message': 'DONT ADD NEW SERVICE'}, 404

        return all_service()

@service.route('/string:<service_name>')
@service.doc(params={'service_name': 'name_service'})
class OneService(Resource):
    def get(self, service_name):
        return get_filter_services(Filter(name_services=[service_name]))

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
        for one_connect in all_data_connect.all_connect:
            new_con = ServiceStaffConnect(*one_connect)
            new_con.save_to_db()


