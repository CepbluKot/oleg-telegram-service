from flask import Blueprint
from flask_restplus import Api
from .booking_ns.booking_ns import booking
from .service_ns.service_ns import service
from .event_ns.event_ns import event
from .staff_ns.staff_ns import staff
from .client_ns.client_ns import client

blueprint = Blueprint('documented_api_booking', __name__, url_prefix='/api_booking')

api_exten = Api(
    blueprint,
    title='Oleg Rest-Api',
    version='1.0',
    description='Oleg Technology',
    doc='/doc'
)

print('test')
api_exten.add_namespace(booking)
api_exten.add_namespace(service)
api_exten.add_namespace(event)
api_exten.add_namespace(staff)
api_exten.add_namespace(client)

