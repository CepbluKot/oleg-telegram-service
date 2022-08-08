from setting_web import ma
from models.all_models import MyService, ServiceStaffConnect


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = MyService
        load_instance = True
        include_relationships = True


class ServiceStaffSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = ServiceStaffConnect
        load_instance = True
        include_relationships = True