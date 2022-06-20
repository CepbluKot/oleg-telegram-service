from flask import Blueprint
from flask_restplus import Api
from routers.namespace.booking_ns import booking
from routers.namespace.service_ns import service

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

