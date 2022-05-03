from main import ModelView, db, admin, flask_app, jwt, get_jwt, verify_jwt_in_request, create_access_token, jwt_required
from functools import wraps

from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from models.all_users_connectall import UsersConnectALL


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


@flask_app.route("/login", methods=["POST"])
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


@flask_app.route("/registers", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    name = request.json.get("password", None)

    hash_password = generate_password_hash(password)
    new_user = UsersConnectALL(name, username, hash_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('Successful registration')
