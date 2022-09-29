from setting_web import flask_app, db
from functools import wraps
from werkzeug.security import generate_password_hash


from flask import jsonify, request
from werkzeug.security import check_password_hash

from ....models.all_models import Users

def _base_query():
    return Users.query


def get_filter_users():
    pass

