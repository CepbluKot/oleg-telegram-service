from flask import jsonify, request
from setting_web import flask_app, db, ma

from api.api_workig_date import *


@flask_app.route('/api/event')
def all_event():
    res_data = all_working_date()
    return jsonify(res_data)