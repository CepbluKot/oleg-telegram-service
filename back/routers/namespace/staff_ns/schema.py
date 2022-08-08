from setting_web import ma
from models.all_models import MyStaff


class StaffSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = MyStaff
        load_instance = True
        include_relationships = True