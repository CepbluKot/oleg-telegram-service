from setting_web import flask_app, db, ma
from back.models.booking_models import AllBooking, Event, ServiceEvent

from back.routers.namespace.event_ns.schema import EventSchema
from back.routers.namespace.service_ns.schema import ServiceSchema
from back.routers.namespace.client_ns.schema import InfoUsersComSchema


class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True
        exclude = ('connect_staff',  )

    connect_user = ma.Nested(InfoUsersComSchema())
    connect_event = ma.Nested(EventSchema(exclude=('event_booking', 'event_se', )))
    connect_service = ma.Nested(ServiceSchema(exclude=('id', 'ssc_service_se', 'service_se', 'service_ab',)))


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = Event
        load_instance = True
        include_relationships = True
        exclude = ('event_se',)

    event_booking = ma.List(ma.Nested(InfoBookingSchema(exclude=('connect_event', 'connect_service', ))))