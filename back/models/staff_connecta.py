from app import db


class MyStaff(db.Model):
    __tablename__ = 'mystaff_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_staff = db.Column(db.String)
    service_staff = db.Column(db.JSON)
    connect_tb = db.relationship('all_booking')