from flask import Blueprint
from flask_restplus import Api
from routers.namespace.users_ns.users_ns import users

blueprint = Blueprint('documented_api', __name__, url_prefix='/api_main')

api_exten = Api(
    blueprint,
    title='Oleg Rest-Api',
    version='1.0',
    description='Oleg Technology',
    doc='/doc'
)

api_exten.add_namespace(users)


