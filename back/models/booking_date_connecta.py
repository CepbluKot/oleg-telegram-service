from main import db, ma


class AllBooking(db.Model):
    __tablenmae__ = 'all_booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Time)

    signup_date = db.Column(db.Integer, db.ForeignKey('days_connecta.id')) #день_записи
    connect_day = db.relationship('Days')

    signup_user = db.Column(db.Integer, db.ForeignKey('users_this_company.id')) #человек который записался
    connect_user = db.relationship('CompanyUsers')

    signup_service = db.Column(db.Integer, db.ForeignKey('myservice_connecta.id'))
    connect_service = db.relationship('MyService')

    signup_staff = db.Column(db.Integer, db.ForeignKey('mystaff_connecta.id'))
    connect_staff = db.relationship('MyStaff')
    comment = db.Column(db.TEXT)




