from setting_web import db, ma


class Days(db.Model):
    __tablename__ = 'days_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Date)
    service_this_day = db.Column(db.JSON)
    staff_free = db.Column(db.ARRAY(db.Integer))

    def __init__(self, day, free_items, staff_free):
        self.day = day
        self.free_items = free_items
        self.staff_free = staff_free

    def __repr__(self):
        return f"Day ('{self.day}')"
