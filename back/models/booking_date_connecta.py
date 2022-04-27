from app import db


class AllBooking(db.Model):
    __tablenmae__ = 'all_booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Time)
    signup_date = db.Column(db.Integer, db.ForeignKey('days_connecta.id')) #день_записи
    signup_user = db.Column(db.Integer, db.ForeignKey('users_this_company.id')) #человек который записался
    signup_service = db.Column(db.Integer, db.ForeignKey('myservice_connecta.id'))
    signup_staff = db.Column(db.Integer, db.ForeignKey('mystaff_connecta.id'))
    comment = db.Column(db.TEXT)