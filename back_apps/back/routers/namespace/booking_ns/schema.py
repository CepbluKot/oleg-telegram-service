from setting_web import ma
from ....models.booking_models import AllBooking, EventDay, EventSetting, CompanyUsers
from marshmallow import fields


class ClientCompanySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = CompanyUsers
        load_instance = True
        include_relationships = True
        #exclude = ('event_day_se', 'event_se', 'weekdays', )


class EventSettingSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventSetting
        load_instance = True
        include_relationships = True
        exclude = ('event_day_se', 'event_se', 'weekdays', )


class InfoBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllBooking
        load_instance = True
        include_relationships = True
        exclude = ('connect_staff',  )

    connect_user = ma.Nested(ClientCompanySchema())
    #connect_service = ma.Nested(ServiceSchema(exclude=('id', 'ssc_service_se', 'service_se', 'service_ab',)))



class EventDaySchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True

    event_booking = ma.List(ma.Nested(InfoBookingSchema(exclude=('connect_event', 'connect_service', ))), required=True)
    connect_event_setting = ma.Nested(EventSettingSchema(), required=True)


class EventDayCorrectDateSchema(ma.SQLAlchemyAutoSchema):
    """Дата класс события"""
    class Meta:
        model = EventDay
        load_instance = True
        include_relationships = True
        exclude = ("event_time_start", "event_time_end",)

    EventDay = ma.Nested(EventDaySchema(exclude=("event_time_start", "event_time_end", "day_end", "day_start", "id",)), data_key="event_setting_booking")
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