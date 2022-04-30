from main import db

class CompanyUsers(db.Model):
    __tablename__ = 'users_this_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_client = db.Column(db.String)
    tg_id = db.Column(db.Integer)
    phone_num = db.Column(db.String)


    def __init__(self, new_name, tg_id, phone_num):
        self.name_client = new_name
        self.tg_id = tg_id
        self.phone_num = phone_num

    def __repr__(self):
        return f"User ('{self.name_client}', {self.tg_id})"

"""
class UsersSchema(ma.Schema):
    class Meta:
        model = CompanyUsers
        sqla_session = db.session
"""