from setting_web import db, flask_app, get_jwt, verify_jwt_in_request, create_access_token, cross_origin
from functools import wraps
from werkzeug.security import generate_password_hash


from flask import jsonify, request
from werkzeug.security import check_password_hash

from models.all_models import UsersConnectALL
from bissnes_logic.insert_data_modul import add_users_connecta


def _base_query():
    return UsersConnectALL.query


def get_filter_users():
    pass

