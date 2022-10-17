from setting_web import ma
from ....models.booking_models import AllBooking, EventDay, EventSetting, CompanyUsers, MyService, ServiceEvent
from ..service_ns.schema import ServiceSchema


class ServiceEventSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс прикрепления к одному дню"""
    class Meta:
        model = ServiceEvent
        load_instance = True
        include_relationships = True

    service_connect = ma.Nested(ServiceSchema(exclude=('service_se', 'duration', 'service_ab', 'ssc_service_se')))


class EventSettingSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventSetting
        load_instance = True
        include_relationships = True
        exclude = ("event_day_se", )

    event_se = ma.List(ma.Nested(ServiceEventSchema(exclude=("event_connect",))))



from setting_web import ma
from ....models.booking_models import AllBooking, EventDay, EventSetting, CompanyUsers, MyService, ServiceEvent
from marshmallow import fields

from datetime import time, timedelta


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
    name_service = fields.String(attribute='service_connect.name_service')

    class Meta:
        model = ServiceEvent
        load_instance = True
        include_relationships = True
        exclude = ('count_service_this_event', 'event_connect', )

    service_connect = ma.Nested(ServiceSchema())


"""  API FOR CALENDAR   """


class ClientCompanySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True

    id = fields.Integer(data_key='id_client')


class EventSettingSchemaCalendar(ma.SQLAlchemyAutoSchema):
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

    correct_booking_time_start = fields.Method("get_time_start")

    def get_time_start(self, obj):
        if hasattr(obj, "booking_time_start"):
            date_iter = obj.booking_day_start
            date_end = obj.booking_day_end

            delta_days = date_end - date_iter

            correct_time_booking = {}

            for iter_day in range((delta_days).days + 2):

                if date_iter == obj.booking_day_start:
                    time_start = obj.booking_time_start
                else:
                    time_start = time(hour=0)

                if date_iter == obj.booking_day_end:
                    time_end = obj.booking_time_end
                elif date_iter < obj.booking_day_end and date_iter >= obj.booking_day_start:
                    time_end = time(hour=23, minute=59)
                else:
                    time_end = time(hour=0)

                correct_time_booking[date_iter.strftime('%Y-%m-%d')] = [time_start, time_end]
                date_iter += timedelta(days=iter_day)

            return correct_time_booking
        return None

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
    connect_event_setting = ma.Nested(EventSettingSchemaCalendar(), required=True, data_key="event_setting")


class EventDayCorrectDateSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True
        exclude = ("event_time_start", "event_time_end",)

    id = fields.Integer(data_key='id_event_day')

    EventDay = ma.Nested(EventDaySchema(exclude=("event_time_start", "event_time_end", "day_end", "day_start", "id",)),
                                        data_key="setting_and_booking")

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