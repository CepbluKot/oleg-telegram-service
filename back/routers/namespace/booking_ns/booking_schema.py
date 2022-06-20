from setting_web import flask_app, db, ma
from models.all_models import AllBooking

from queries.queries_workig_date import find_boundaries_week, EventSchema
from queries.queries_client_company import InfoUsersComSchema
from queries.queries_services import ServiceSchema


class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True

    connect_user = ma.Nested(InfoUsersComSchema())
    connect_event = ma.Nested(EventSchema())
    connect_service = ma.Nested(ServiceSchema())