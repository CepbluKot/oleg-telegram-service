from flask import request
from flask_restplus import Namespace, Resource, fields

from models.all_models import MyService
from .queries_services import all_service, get_filter_services
from .dataclass_services import FilterServices as Filter

service = Namespace('service')


add_service = service.model('AllService', {
     "name_service": fields.String(description='new_service', required=True),
     "price": fields.Float()
})


@service.route('')
class AllService(Resource):
    def get(self):
        return all_service()

    @service.expect(add_service)
    def post(self):
        new_service = MyService(**request.get_json())
        new_service.save_to_db()

        return all_service()


service_filter = service.model('AddService', {
     "name_service": fields.List(fields.String(description='filter services', required=True)),
     "name_staff": fields.List(fields.String(description='filter staff', required=True))
})


@service.route('/filter')
class FilterServices(Resource):
    @service.expect(service_filter)
    def post(self):
        add_filter = Filter(**request.get_json())
        res_data = get_filter_services(add_filter)
        return res_data
