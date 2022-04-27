from app import db


class Days(db.Model):
    __tablename__ = 'days_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Date)
    free_items = db.Column(db.Integer)
    staff_free = db.Column(db.JSON)
    connect_tb = db.relationship('all_booking', lazy=True)

    def __init__(self, day, free_items, staff_free):
        self.day = day
        self.free_items = free_items
        self.staff_free = staff_free
