from setting_web import flask_app, Blueprint
from flask_restplus import Api
from routers.namespace import blueprint

from routers import admin_tools
flask_app.register_blueprint(blueprint)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
