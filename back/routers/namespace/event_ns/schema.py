from setting_web import ma
from models.all_models import ServiceEvent, Event

from routers.namespace.service_ns.schema import ServiceSchema

class ServiceEventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс прикрепления к одному дню"""
    class Meta:
        model = ServiceEvent
        load_instance = True
        include_relationships = True

    service_connect = ma.Nested(ServiceSchema(exclude=('service_se',)))


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = Event
        load_instance = True
        include_relationships = True

    event_se = ma.List(ma.Nested(ServiceEventSchema(exclude=("event_connect",))))