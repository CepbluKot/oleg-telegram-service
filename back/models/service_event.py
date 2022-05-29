from setting_web import db


class ServiceEvent(db.Model):
    __tablenmae__ = 'all_booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_company.id'), nullable=False)
    event_connect = db.relationship('Event', backref='event_se')

    service_id = db.Column(db.Integer, db.ForeignKey('myservice_connecta.id'), nullable=False)
    service_connect = db.relationship('MyService', backref='service_se', lazy='joined')

    quantity = db.Column(db.Integer, nullable=False)




