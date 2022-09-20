from setting_web import db, config
from datetime import timedelta, date
from calendar import weekday
from typing import List, Optional
import rapidjson
import enum


ROLE_EMPLOYEE = 0
ROLE_ADMIN = 1


class Users(db.Model):
    __tablename__ = 'global_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String)
    tg_id = db.Column(db.Integer)
    role = db.Column(db.Integer, default=ROLE_EMPLOYEE)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Unicode, nullable=False)

    def __init__(self, new_name, login, hash_password, role=ROLE_EMPLOYEE):
        self.name = new_name
        self.login = login
        self.role = role
        self.password = hash_password
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_login(cls, login)->'Users':
        return cls.query.filter(cls.login == login).first()


class Department(db.Model):
    __tablename__ = 'department_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    ip_service = db.Column(db.String)

    def __init__(self, name, ip_serv, config_password):
        if config_password == config['main']['password']:
            try:
                self.name = name
                self.ip_service = ip_serv
                self.save_to_db()
            except:
                print('Error: db connect')
        else:
            print('Error: authorization')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Department ('{self.name}')"

    @classmethod
    def find_by_department(cls, name)->'Department':
        return cls.query.filter(cls.name == name).first()


class UserConnectDepartment(db.Model):
    __tablename__ = 'connect_department'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('global_users.id'))
    connect_user = db.relationship('Users')

    department_id = db.Column(db.Integer, db.ForeignKey('department_info.id'))
    connect_department = db.relationship('Department')

    def __init__(self, user_login, name_department):
        info_department = Department.find_by_department(name_department)
        info_user = Users.find_by_login(user_login)

        if info_department and info_user:
            try:
                self.user_id = info_user.id
                self.department_id = info_department.id
                self.save_to_db()
            except:
                print('Error: db adder or connect in UserConnectDepartment')
        else:
            print('Error: find department or user')

    @classmethod
    def check_connect(cls, department_id, user_id):
        query_connect = cls.query.filter(db.and_(cls.user_id == user_id, cls.department_id == department_id))
        if query_connect:
            return True
        else:
            return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



