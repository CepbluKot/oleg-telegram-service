from .service_schema import ServiceSchema
from models.all_models import *

from .dataclass_services import FilterServices as Filter


def _base_query():
    res_query = MyService.query
    return res_query


def all_service():
    all_service_data = _base_query()
    api_all_booking_schema = ServiceSchema(many=True)

    return api_all_booking_schema.dump(all_service_data)


def get_filter_services(new_filter: Filter):
    data_services = _base_query()

    if new_filter.name_services is not None:
        data_services = data_services.filter(MyService.name_service.in_(new_filter.name_services))

    if new_filter.name_staff is not None:
        data_services = data_services.filter(MyStaff.name_staff.in_(new_filter.name_staff))

    api_all_booking_schema = ServiceSchema(many=True)
    return api_all_booking_schema.dump(data_services)


def check_exit_service(name_service):
    status = _base_query().filter_by(MyService.name_service == name_service).first() is not None
    return status

