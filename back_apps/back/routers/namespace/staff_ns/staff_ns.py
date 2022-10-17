from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse
from pydantic import ValidationError

from setting_web import token_required, cross_origin
from ....models.booking_models import MyStaff
from .queries import all_staff, filter_staff
from .validate import ValidateStaff, FilterStaff

staff = Namespace('staff')

add_staff = staff.model('data_one_staff', {
    "name_staff": fields.String(discriminator='name staff')
})


@staff.route('')
class AllStaff(Resource):
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @staff.doc(security='apikey')
    @token_required
    def get(self):
        return all_staff()

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @staff.doc(security='apikey')
    @token_required
    @staff.expect(add_staff)
    def post(self):
        try:
            new_staff = ValidateStaff(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        MyStaff(**request.get_json())
        return filter_staff(FilterStaff(name_staff=[new_staff.name_staff]))


@staff.route('/one_staff')
@staff.doc(params={'id_staff': 'id_staff'})
class OneStaff(Resource):
    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @staff.doc(security='apikey')
    @token_required
    def get(self, id_staff):
        staff_url_parse = reqparse.RequestParser()
        staff_url_parse.add_argument('id_staff', type=int)

        id_staff = staff_url_parse.parse_args()["id_staff"]

        if id_staff:
            req_data = filter_staff(FilterStaff(id=[id_staff]))

            if req_data:
                return jsonify(req_data), 20
            else:
                return {"message": "not find data"}, 404

        else:
            return {"message": "not correct input data"}, 400

        return filter_staff(FilterStaff(id=[id_staff])), 200

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @staff.doc(security='apikey')
    @token_required
    @staff.expect(add_staff)
    def put(self):
        staff_url_parse = reqparse.RequestParser()
        staff_url_parse.add_argument('id_staff', type=int)

        id_staff = staff_url_parse.parse_args()["id_staff"]

        try:
            new_staff = ValidateStaff(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        find_sf = MyStaff.find_my_id(id_staff)

        if find_sf:
            find_sf.name_staff = new_staff.name_staff
            find_sf.update_from_db()
            return jsonify(filter_staff(FilterStaff(id=[id_staff]))), 200

        return {'ERROR': "STAFF NOT FIND"}, 404

    @cross_origin(origins=["*"], supports_credentials=True, automatic_options=False)
    @staff.doc(security='apikey')
    @token_required
    def delete(self):
        staff_url_parse = reqparse.RequestParser()
        staff_url_parse.add_argument('id_staff', type=int)

        id_staff = staff_url_parse.parse_args()["id_staff"]

        find_sf = MyStaff.find_my_id(id_staff)
        if find_sf:
            try:
                find_sf.delete_from_db()
                return {'message': "STAFF DELETE"}, 200
            except:
                return {'ERROR': "STAFF NOT FIND"}, 404

        return {'ERROR': "STAFF NOT FIND"}, 404


