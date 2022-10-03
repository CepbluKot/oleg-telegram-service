from flask import Blueprint, request
from functools import wraps
from flask_restplus import Api
from .booking_ns.booking_ns import booking
from .service_ns.service_ns import service
from .event_ns.event_ns import event
from .staff_ns.staff_ns import staff
from .client_ns.client_ns import client

from setting_web import head_conf

blueprint = Blueprint('documented_api_booking', __name__, url_prefix='/api_booking')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_input = None

        if 'X-API-KEY' in request.headers:
            token_input = request.headers['X-API-KEY']

        if not token_input:
            return {'message': 'Not have token, give me please'}

        if token_input != head_conf.password_swag:
            return {'message': 'token not correct'}, 403

        return f(*args, **kwargs)
    return decorated


api_exten = Api(
    blueprint,
    title='Oleg Rest-Api',
    version='1.0',
    description='Oleg Technology',
    doc='/doc',
    security='apikey',
    authorizations=head_conf.auth_setting_swagger
)

api_exten.add_namespace(booking)
api_exten.add_namespace(service)
api_exten.add_namespace(event)
api_exten.add_namespace(staff)
api_exten.add_namespace(client)

