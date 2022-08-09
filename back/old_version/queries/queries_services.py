from setting_web import db, ma
from models.all_models import *



def _base_query():
    res_query = db.session.query(MyService)
    return res_query


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = MyService
        load_instance = True
        include_relationships = True


def all_service():
    all_service_data = _base_query()
    api_all_booking_schema = ServiceSchema(many=True)

    return api_all_booking_schema.dump(all_service_data)


def get_filter_services(name_staff=None, name_service=None):
    data_services = _base_query()

    if name_service != None:
        data_services = data_services.filter(MyService.name_service == name_service)

    if name_staff != None:
        query_staff_ar = db.session.query(MyStaff.service_staff).filter(MyStaff.name_staff == name_staff).all()
        service_staff = query_staff_ar[0][0]

        data_services = data_services.filter(MyService.id == db.any_(service_staff))

    api_all_booking_schema = ServiceSchema(many=True)
    return api_all_booking_schema.dump(data_services)


def check_exit_service(name_service):
    status = _base_query().filter_by(MyService.name_service == name_service).first() is not None
    return status

