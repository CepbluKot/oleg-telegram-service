from setting_web import db


class DefaultSetting(db.Model):
    __tablename__ = 'default_setting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_event = db.Column(db.Time)
    end_event = db.Column(db.Time)
    delta_time = db.Column(db.Time)
    default_services = db.Column(db.JSON)

    def __int__(self, start_event, end_event, delta_time, default_services):
        self.start_event = start_event
        self.end_event = end_event
        self.delta_time = delta_time
        self.default_services = default_services

