from app import db


class MyService(db.Model):
    __tablename__ = 'myservice_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_service = db.Column(db.String)
    price_service = db.Column(db.DECIMAL)
    connect_tb = db.relationship('all_booking', lazy=True)