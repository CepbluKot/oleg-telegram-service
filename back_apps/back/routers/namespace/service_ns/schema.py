from setting_web import ma
from ....models.booking_models import MyService, ServiceStaffConnect


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = MyService
        load_instance = True
        include_relationships = True
        exclude = ('service_ab', 'ssc_service_se', 'service_se', )

class ServiceStaffSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = ServiceStaffConnect
        load_instance = True
        include_relationships = True