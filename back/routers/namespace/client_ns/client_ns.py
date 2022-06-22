from flask_restplus import Resource, Namespace, fields
from flask import request

from .dataclass_client import RegisterСlient
from .dataclass_client import FilterClient as Filter
from .dataclass_client import FilterClientBooking as FilterInBooking
from .queries_client import get_filter_client, all_client

client = Namespace('client', 'api about client for users')

client_add = client.model('AddClient', {
    "tg_id": fields.Integer(),
    "phone": fields.String(),
    "name": fields.String()
})


@client.route('')
class Client(Resource):
    def get(self):
        return all_client()

    @client.expect(client_add)
    def post(self):
        new_client = RegisterСlient(**request.get_json())

    def put(self):
        pass


@client.route('/filter')
class ClientFilter(Resource):
    def post(self):
        pass


client_filter_booking = client.model('AddClient', {
    "tg_id": fields.List(fields.Integer()),
    "phone": fields.List(fields.String()),
    "name": fields.List(fields.String())
})

@client.route('/filter/booking')
class ClientFilterBooking(Resource):
    def post(self):
        pass





