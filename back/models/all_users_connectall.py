from app import db


ROLE_EMPLOYEE = 0
ROLE_ADMIN = 1

class UsersConnectALL(db.Model):
    __tablename__ = 'users_connectall'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String)
    tg_id = db.Column(db.Integer)
    role = db.Column(db.Integer, default=ROLE_EMPLOYEE)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.Unicode, nullable=False)

    def __init__(self, new_name, new_tg, new_login, password, role=ROLE_EMPLOYEE):
        self.name = new_name
        self.tg_id = new_tg
        self.login = new_login
        self.role = role
        self.password = password