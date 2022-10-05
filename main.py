from setting_web import flask_app
from back.routers.namespace import blueprint as booking_blueprint
from back_users.routers.namespace import blueprint as booking_users


from back_users.routers import admin_tools as at2
flask_app.register_blueprint(booking_blueprint)
flask_app.register_blueprint(booking_users)
from back.routers import admin_tools as at1


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0')
