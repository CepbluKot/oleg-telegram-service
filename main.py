from setting_web import flask_app, Blueprint
from flask import jsonify
from flask_restplus import Api
from back.routers.namespace import blueprint as booking_blueprint
from back_users.routers.namespace import blueprint as booking_users


from back.routers import admin_tools as at1
#from back_users.routers import admin_tools as at2
flask_app.register_blueprint(booking_blueprint)
flask_app.register_blueprint(booking_users)

@flask_app.route('/')
def get_test():
    return jsonify('heeei')


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
