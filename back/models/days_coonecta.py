from main import db, ma
from models.booking_date_connecta import AllBooking


class Days(db.Model):
    __tablename__ = 'days_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Date)
    free_items = db.Column(db.Integer)
    staff_free = db.Column(db.ARRAY(db.Integer))

    def __init__(self, day, free_items, staff_free):
        self.day = day
        self.free_items = free_items
        self.staff_free = staff_free

    def __repr__(self):
        return f"Day ('{self.day}')"


class DaysShema(ma.Schema):
    class Meta:
        fields = ('id', 'day', 'free_items', 'staff_free')
