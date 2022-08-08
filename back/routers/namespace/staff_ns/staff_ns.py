from flask import request
from flask_restplus import Namespace, Resource, fields
from pydantic import ValidationError

from models.all_models import MyStaff
from .queries import all_staff, filter_staff
from .validate import ValidateStaff, FilterStaff

staff = Namespace('staff')

add_staff = staff.model('data_one_staff', {
    "name_staff": fields.String(discriminator='name staff')
})


@staff.route('')
class AllStaff(Resource):
    def get(self):
        return all_staff()

    @staff.expect(add_staff)
    def post(self):
        try:
            new_staff = ValidateStaff(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        MyStaff(**request.get_json())
        return filter_staff(FilterStaff(name_staff=[new_staff.name_staff]))


@staff.route('/int:<id_staff>')
@staff.doc(params={'id_staff': 'id_staff'})
class OneStaff(Resource):
    def get(self, id_staff):
        return filter_staff(FilterStaff(id=[id_staff])), 200

    @staff.expect(add_staff)
    def put(self, id_staff):
        try:
            new_staff = ValidateStaff(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        find_sf = MyStaff.find_my_id(id_staff)

        if find_sf:
            find_sf.name_staff = new_staff.name_staff
            find_sf.update_from_db()
            return filter_staff(FilterStaff(id=[id_staff])), 200

        return {'ERROR': "STAFF NOT FIND"}, 404

    def delete(self, id_staff):
        find_sf = MyStaff.find_my_id(id_staff)
        if find_sf:
            try:
                find_sf.delete_from_db()
                return {'message': "STAFF DELETE"}, 200
            except:
                return {'ERROR': "STAFF NOT FIND"}, 404

        return {'ERROR': "STAFF NOT FIND"}, 404


