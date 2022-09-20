from setting_web import ma
from back.models.booking_models import CompanyUsers


class InfoUsersComSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True
