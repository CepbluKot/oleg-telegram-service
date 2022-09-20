from flask_restplus import Resource, Namespace, fields
from flask import request
from pydantic import ValidationError

from back.models.booking_models import CompanyUsers
from .validate import RegisterClient, FilterClient as Filter
from .queries import get_filter_client, all_client

client = Namespace('client', 'api about client for users')

client_info = client.model('Data Info Client Company', {
    "tg_id": fields.Integer(),
    "phone": fields.String(),
    "name": fields.String()
})

"""Функции выносятся вне класса, для общения с  тг ботом"""


def add_client(new_cl: dict):
    try:
        new_client = RegisterClient(**new_cl)
    except ValidationError as e:
        return {"message": e.json()}, 404

    CompanyUsers(new_name=new_client.name,
                 tg_id=new_client.tg_id,
                 phone_num=new_client.phone)

    return get_filter_client(Filter(tg_id=[new_client.tg_id])), 200


def update_client(upd_cl: dict):
    print(upd_cl)
    try:
        upd_client = RegisterClient(**upd_cl)
    except ValidationError as e:
        return {"message": e.json()}, 404

    find_client = CompanyUsers.find_by_tg_id(upd_client.tg_id)
    if find_client:
        if upd_client.name is not None:
            find_client.name_client = upd_client.name
        elif upd_client.phone is not None:
            find_client.phone_num = upd_client.phone

        find_client.update_from_db()
        return get_filter_client(Filter(tg_id=[upd_client.tg_id])), 200
    else:
        return {"message": "NOT FIND USERS"}, 404


@client.route('')
class Client(Resource):
    def get(self):
        return all_client()

    @client.expect(client_info)
    def post(self):
        return add_client(request.get_json())

    @client.expect(client_info)
    def put(self):
        return update_client(request.get_json())


@client.route('/int:<tg_id>')
@client.doc(params={'tg_id': 'user tg id'})
class OneClient(Resource):
    def get(self, tg_id):
        return get_filter_client(Filter(tg_id=[int(tg_id)])), 200


client_filter_booking = client.model('FilterClient', {
    "tg_id": fields.List(fields.Integer()),
    "phone": fields.List(fields.String()),
    "name": fields.List(fields.String())
})


@client.route('/filter')
class ClientFilter(Resource):
    @client.expect(client_filter_booking)
    def post(self):
        try:
            filter_data = Filter(**request.get_json())
        except ValidationError as e:
            return {"messenge": e.json()}, 404

        return get_filter_client(filter_data)





