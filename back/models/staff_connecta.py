from main import db


class MyStaff(db.Model):
    __tablename__ = 'mystaff_connecta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_staff = db.Column(db.String)
    service_staff = db.Column(db.ARRAY(db.Integer))

    def __repr__(self):
        return f"Staff ('{self.name_staff}')"