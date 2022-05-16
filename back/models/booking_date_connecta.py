from setting_web import db


class AllBooking(db.Model):
    __tablenmae__ = 'all_booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

    signup_date = db.Column(db.Integer, db.ForeignKey('days_connecta.id')) #день_записи
    connect_day = db.relationship('Days')

    signup_user = db.Column(db.Integer, db.ForeignKey('users_this_company.id')) #человек который записался
    connect_user = db.relationship('CompanyUsers')

    signup_service = db.Column(db.Integer, db.ForeignKey('myservice_connecta.id')) #услуга
    connect_service = db.relationship('MyService')

    signup_staff = db.Column(db.Integer, db.ForeignKey('mystaff_connecta.id')) #тренер
    connect_staff = db.relationship('MyStaff')
    comment = db.Column(db.TEXT)

    def __init__(self, signup_date, signup_user, signup_service, time_start, time_end):
        self.signup_date = signup_date
        self.signup_service = signup_service
        self.signup_user = signup_user
        self.time_start = time_start
        self.time_end = time_end
        #self.connect_day = connect_day





