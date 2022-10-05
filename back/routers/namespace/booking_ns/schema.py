from setting_web import ma
from ....models.booking_models import AllBooking, EventDay, EventSetting

from ..service_ns.schema import ServiceSchema
from ..client_ns.schema import InfoUsersComSchema


class EventSettingSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True

class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True
        exclude = ('connect_staff',  )

    connect_user = ma.Nested(InfoUsersComSchema())
    connect_service = ma.Nested(ServiceSchema(exclude=('id', 'ssc_service_se', 'service_se', 'service_ab',)))


class EventDaySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True
        exclude = ('event_se',)

    event_booking = ma.List(ma.Nested(InfoBookingSchema(exclude=('connect_event', 'connect_service', ))))
    connect_event_setting = ma.Nested(EventSettingSchema())