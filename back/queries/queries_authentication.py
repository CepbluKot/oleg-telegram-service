from setting_web import db, flask_app, get_jwt, verify_jwt_in_request, create_access_token, cross_origin
from functools import wraps

from flask import jsonify, request
from werkzeug.security import check_password_hash

from models.users_oleg.all_users_connectall import UsersConnectALL
from bissnes_logic.insert_data_modul import add_users_connecta

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


@flask_app.route("/login", methods=["POST", "OPTIONS"])
@cross_origin(origins=["*"], supports_credentials=True)
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


@flask_app.route("/register", methods=["POST"])
@cross_origin(origins=["*"], supports_credentials=True)
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)

    return jsonify(add_users_connecta(password, username, name))