from setting_web import db, config
from datetime import timedelta, date
from calendar import weekday
from typing import List, Optional
import rapidjson
import enum

from .booking_models import *

# ROLE_EMPLOYEE = 0
# ROLE_ADMIN = 1
#
#
# class Users(db.Model):
#     __tablename__ = 'global_users'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     company_id = db.Column(db.Integer)
#     name = db.Column(db.String)
#     tg_id = db.Column(db.Integer)
#     role = db.Column(db.Integer, default=ROLE_EMPLOYEE)
#     login = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.Unicode, nullable=False)
#
#     # default_set = db.Column(db.Integer, db.ForeignKey('default_setting.id'))
#     # connect_default = db.relationship('DefaultSetting')
#
#     def __init__(self, new_name, login, hash_password, role=ROLE_EMPLOYEE):
#         self.name = new_name
#         self.login = login
#         self.role = role
#         self.password = hash_password
#         self.save_to_db()
#
#
# class Department(db.Model):
#     _tablename__ = 'department_info'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String, unique=True, nullable=False)
#     ip_service = db.Column(db.String)
#
#
#
#
# class UserConnectDepartment(db.Model):
#     __tablename__ = 'connect_department'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('global_users.id'))
#     connect_user = db.relationship('Users')
#
#     department_id = db.Column(db.Integer, db.ForeignKey('department_info.id'))
#     connect_department = db.relationship('Department')
#
#
#
#
# # if config["Booking"]["power_status"]:
# #     from .booking_models import *

