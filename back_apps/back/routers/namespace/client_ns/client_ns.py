from flask_restx import Resource, Namespace, fields, reqparse
from flask import request, jsonify
from pydantic import ValidationError
from setting_web import cross_origin, token_required
from sqlalchemy.exc import IntegrityError, PendingRollbackError


from ....models.booking_models import CompanyUsers
from .validate import RegisterClient, FilterClient as Filter
from .queries import get_filter_client, all_client

client = Namespace('client', 'api about client for users')

client_info = client.model('Data Info Client Company', {
    "tg_id": fields.Integer(),
    "phone": fields.String(),
    "name": fields.String()
})


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
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @client.doc(security='apikey')
    @token_required
    def get(self):
        return jsonify(all_client())

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @client.doc(security='apikey')
    @token_required
    @client.expect(client_info)
    def post(self):
        try:
            new_client = RegisterClient(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        try:
            CompanyUsers(new_name=new_client.name,
                         tg_id=new_client.tg_id,
                         phone_num=new_client.phone)

            req_data = get_filter_client(Filter(tg_id=[new_client.tg_id]))

            if req_data:
                return jsonify(req_data), 200
            else:
                return {"message": "maybe don't correct input data"}, 400

        except PendingRollbackError:
            return {"message": "this event alredy exist"}, 401
        except IntegrityError:
            return {"message": "this event alredy exist"}, 401

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @client.doc(security='apikey')
    @token_required
    @client.expect(client_info)
    def put(self):
        try:
            upd_client = RegisterClient(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        find_client = CompanyUsers.find_by_tg_id(upd_client.tg_id)
        if find_client:
            if upd_client.name is not None:
                find_client.name_client = upd_client.name
            elif upd_client.phone is not None:
                find_client.phone_num = upd_client.phone

            find_client.update_from_db()
            return jsonify(get_filter_client(Filter(tg_id=[upd_client.tg_id]))), 200
        else:
            return {"message": "NOT FIND USERS"}, 404


@client.route('/info_client')
class OneClient(Resource):
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @client.doc(security='apikey')
    @client.doc(params={'tg_id': 'telegram id'})
    @token_required
    def get(self):
        client_url_parse = reqparse.RequestParser()
        client_url_parse.add_argument('tg_id', type=int)

        tg_id: int = client_url_parse.parse_args()['tg_id']
        if tg_id:
            try:
                req_data = get_filter_client(Filter(tg_id=[int(tg_id)]))

                if len(req_data) == 0:
                    return {"message": "not find tg_id"}, 404

                return jsonify(req_data), 200

            except ValueError:
                return {"message": "not correct data"}, 401
        else:
            return {"message": "not correct input data"}, 400


client_filter_booking = client.model('FilterClient', {
    "tg_id": fields.List(fields.Integer()),
    "phone": fields.List(fields.String()),
    "name": fields.List(fields.String())
})


@client.route('/filter')
class ClientFilter(Resource):
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @client.doc(security='apikey')
    @token_required
    @client.expect(client_filter_booking)
    def post(self):
        try:
            filter_data = Filter(**request.get_json())
        except ValidationError as e:
            return {"messange": e.json()}, 404

        return get_filter_client(filter_data)





