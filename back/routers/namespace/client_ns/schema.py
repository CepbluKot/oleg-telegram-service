from setting_web import ma
from models.all_models import CompanyUsers


class InfoUsersComSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True
