from flask import request
from flask_restplus import Resource, Namespace, fields

from .queries_users import login, register
from .dataclass_users import RegisterUser, Login

from pydantic import ValidationError


users = Namespace('users', description='API for users Oleg')

users_register = users.model('UsersRegister', {
    "name": fields.String(),
    "login": fields.String(),
    "password": fields.String()
})

@users.route('register')
class Register(Resource):
    @users.expect(users_register)
    def post(self):
        try:
            new_user = RegisterUser(**request.get_json())
            return register(new_user)
        except ValidationError as error:
            return error.json(indent=5)