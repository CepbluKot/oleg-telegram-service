from setting_web import flask_app, db

from flask_admin.contrib.sqla import ModelView
from flask import Response
from werkzeug.exceptions import HTTPException

from ..models.all_models import *


class AuthException(HTTPException):
    def __int__(self, message):
        super().__init__(message, Response(
            message, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}))

"""
class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())
"""


class EventView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    create_modal = True
    edit_modal = True


admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view((ModelView(UserConnectDepartment, db.session)))



