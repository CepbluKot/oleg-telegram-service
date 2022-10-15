from setting_web import ma
from ....models.booking_models import AllBooking, EventDay, EventSetting, CompanyUsers, MyService, ServiceEvent
from marshmallow import fields


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    class Meta:
        model = MyService
        load_instance = True
        include_relationships = True
        exclude = ('service_ab', 'ssc_service_se', 'service_se', )


class ServiceEventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс сервиса"""
    id_service = fields.Integer(attribute='service_connect.id')
    max_booking = fields.Integer(attribute='service_connect.max_booking')
    price_service = fields.Float(attribute='service_connect.price_service')
    duration = fields.Time(attribute='service_connect.duration')

    class Meta:
        model = ServiceEvent
        load_instance = True
        include_relationships = True
        exclude = ('count_service_this_event', 'event_connect', )

    service_connect = ma.Nested(ServiceSchema())


class ClientCompanySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True

    id = fields.Integer(data_key='id_client')


class EventSettingSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventSetting
        load_instance = True
        include_relationships = True
        exclude = ('event_day_se',)

    id = fields.Integer(data_key='id_global_event')
    event_se = ma.List(ma.Nested(ServiceEventSchema(exclude = ('service_connect',))), data_key='all_services')


class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True
        exclude = ('connect_staff',)

    id = fields.Integer(data_key='id_booking')

    connect_user = ma.Nested(ClientCompanySchema())
    connect_service = ma.Nested(ServiceSchema(exclude=('ssc_service_se', 'service_se', 'service_ab', 'max_booking',
                                                       'price_service', 'duration',)), data_key="subscription_service")



class EventDaySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True

    event_booking = ma.List(ma.Nested(InfoBookingSchema(exclude=('connect_event', ))), required=True)
    connect_event_setting = ma.Nested(EventSettingSchema(), required=True, data_key="event_setting")


class EventDayCorrectDateSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True
        exclude = ("event_time_start", "event_time_end",)

    id = fields.Integer(data_key='id_event_day')

    EventDay = ma.Nested(EventDaySchema(exclude=("event_time_start", "event_time_end", "day_end", "day_start", "id",)), data_key="setting_and_booking")
    AllBooking = ma.Nested(InfoBookingSchema(exclude=('connect_event', 'connect_service',)))

    correct_time_end = fields.Method("get_data_end")
    correct_time_start = fields.Method("get_data_start")

    def get_data_end(self, obj):
        if hasattr(obj, "correct_time_end"):
            return obj.correct_time_end
        return None

    def get_data_start(self, obj):
        if hasattr(obj, "correct_time_start"):
            return obj.correct_time_start
        return None