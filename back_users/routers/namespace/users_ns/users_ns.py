from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from pydantic import ValidationError

from back_users.models.all_models import Users
from .validate import ValidateRegister, ValidateLogin
from setting_web import db, flask_app, get_jwt, verify_jwt_in_request, create_access_token, cross_origin


users = Namespace('users', description='API for users Oleg')

users_register = users.model('UsersRegister', {
    "name": fields.String(),
    "login": fields.String(),
    "password": fields.String()
})


@users.route('/register')
class Register(Resource):
    @users.expect(users_register)
    def post(self):
        try:
            new_user = ValidateRegister(**request.get_json())
        except ValidationError as error:
            return {"message": error.json(indent=5)}, 200

        try:
            new_user.hash_password = generate_password_hash(new_user.password)
            Users(new_name=new_user.name,
                            login=new_user.login,
                            hash_password=new_user.hash_password)
        except:
            return {"message": "NOT CREATED USERS"}, 404
        return {"message": "GOOD CREATED USERS"}, 200


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator
    return wrapper


users_login = users.model('Login Data Users', {
    "login": fields.String(),
    "password": fields.String()
})


@users.route('/login')
class Login(Resource):
    @users.expect(users_login)
    def post(self):
        try:
            login_us = ValidateLogin(**request.get_json())
        except ValidationError as e:
            return {"message": e.json()}, 404

        find_user = Users.find_by_login(login_us.login)
        if find_user:
            if check_password_hash(find_user.password, login_us.password):
                access_token = create_access_token(
                    "admin_user", additional_claims={"is_administrator": True}
                )
                return {'access_token': access_token}, 200
            else:
                return {"message": "YOU PASSWORD NOT CORRECT"}, 404
        else:
            return {"message", "USER NOT FIND"}, 404

