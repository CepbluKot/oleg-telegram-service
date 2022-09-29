from .. import ma
from . import CompanyUsers


class InfoUsersComSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True
