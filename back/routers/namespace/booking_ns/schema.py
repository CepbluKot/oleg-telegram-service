from setting_web import flask_app, db, ma
from models.all_models import AllBooking

from routers.namespace.event_ns.schema import EventSchema
from routers.namespace.service_ns.schema import ServiceSchema
from routers.namespace.client_ns.schema import InfoUsersComSchema


class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True

    connect_user = ma.Nested(InfoUsersComSchema())
    connect_event = ma.Nested(EventSchema())
    connect_service = ma.Nested(ServiceSchema())