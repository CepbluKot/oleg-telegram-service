from .. import ma
from . import ServiceEvent, Event
from ..service_ns.schema import ServiceSchema


class ServiceEventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс прикрепления к одному дню"""
    class Meta:
        model = ServiceEvent
        load_instance = True
        include_relationships = True

    service_connect = ma.Nested(ServiceSchema(exclude=('service_se', 'duration', 'service_ab', 'ssc_service_se')))


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = Event
        load_instance = True
        include_relationships = True

    event_se = ma.List(ma.Nested(ServiceEventSchema(exclude=("event_connect",))))