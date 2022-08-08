from flask import Blueprint
from flask_restplus import Api
from routers.namespace.booking_ns.booking_ns import booking
from routers.namespace.service_ns.service_ns import service
from routers.namespace.event_ns.event_ns import event
from routers.namespace.staff_ns.staff_ns import staff
from routers.namespace.users_ns.users_ns import users
from routers.namespace.client_ns.client_ns import client

blueprint = Blueprint('documented_api', __name__, url_prefix='/documented_api')

api_exten = Api(
    blueprint,
    title='Oleg Rest-Api',
    version='1.0',
    description='Oleg Technology',
    doc='/doc'
)

api_exten.add_namespace(booking)
api_exten.add_namespace(service)
api_exten.add_namespace(event)
api_exten.add_namespace(staff)
api_exten.add_namespace(client)
api_exten.add_namespace(users)


