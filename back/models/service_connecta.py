from setting_web import db


class MyService(db.Model):
    __tablename__ = 'myservice_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_service = db.Column(db.String, unique=True)
    price_service = db.Column(db.DECIMAL)


    def __init__(self, name_service, price):
        self.name_service = name_service
        self.price_service = price


    def __repr__(self):
        return f"Service ('{self.name_service}')"