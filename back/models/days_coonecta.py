from setting_web import db, ma


class Event(db.Model):
    __tablename__ = 'event_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_event = db.Column(db.String, default="Work_Day")
    day = db.Column(db.Date)
    start_event = db.Column(db.Time)
    end_event = db.Column(db.Time)
    delta = db.Column(db.Time)
    staff_free = db.Column(db.ARRAY(db.Integer))

    def __init__(self, day, start_event, end_event, service_this_day, staff_free=None):
        self.day = day
        self.start_event = start_event
        self.end_event = end_event
        self.service_this_day = service_this_day
        self.staff_free = staff_free

    def __repr__(self):
        return f"Event ('{self.name_event, self.day}')"
