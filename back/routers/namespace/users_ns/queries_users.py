from setting_web import db, flask_app, get_jwt, verify_jwt_in_request, create_access_token, cross_origin
from functools import wraps
from werkzeug.security import generate_password_hash


from flask import jsonify, request
from werkzeug.security import check_password_hash

from models.all_models import UsersConnectALL
from bissnes_logic.insert_data_modul import add_users_connecta

from .dataclass_users import RegisterUser

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


def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    query_user = db.session.query(UsersConnectALL)
    query_user = query_user.filter(UsersConnectALL.login == username).first()

    if query_user != None:
        if check_password_hash(query_user.password, password):
            access_token = create_access_token(
                "admin_user", additional_claims={"is_administrator": True}
            )
            return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401


def register(new_users: RegisterUser):
    try:
        new_users.hash_password = generate_password_hash(RegisterUser.password)
        new_obj_user = UsersConnectALL(new_users.name, new_users.login, new_users.hash_password)
        new_obj_user.save_to_db()
    except:
        return {"Error": "register"}

    return {"Success": "register"}