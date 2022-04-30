from main import ModelView, db, admin, flask_app, jwt, get_jwt, verify_jwt_in_request, create_access_token, jwt_required
from functools import wraps

from flask import jsonify, request


from models.days_coonecta import Days
from models.all_users_this_connecta import CompanyUsers
from models.service_connecta import MyService
from models.staff_connecta import MyStaff
from models.booking_date_connecta import AllBooking
from models.all_users_connectall import UsersConnectALL


admin.add_view(ModelView(Days, db.session))
admin.add_view(ModelView(CompanyUsers, db.session))
admin.add_view(ModelView(MyService, db.session))
admin.add_view(ModelView(MyStaff, db.session))
admin.add_view(ModelView(UsersConnectALL, db.session))
admin.add_view(ModelView(AllBooking, db.session))


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
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(
        "admin_user", additional_claims={"is_administrator": True}
    )
    return jsonify(access_token=access_token)


@flask_app.route("/protected", methods=["GET"])
@admin_required()
def protected():
    return jsonify(foo="bar")

