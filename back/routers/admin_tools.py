from setting_web import admin
from flask_admin.contrib.sqla import ModelView
from flask import Response
from werkzeug.exceptions import HTTPException

from ..models.booking_models import *


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

    #column_sortable_list = ['created_at']


admin.add_view(ModelView(DefaultSetting, db.session))
admin.add_view(EventView(Event, db.session))
admin.add_view(ModelView(CompanyUsers, db.session))
admin.add_view(ModelView(MyService, db.session))
admin.add_view(ModelView(MyStaff, db.session))
#admin.add_view(ModelView(UsersConnectALL, db.session))
admin.add_view(ModelView(AllBooking, db.session))
admin.add_view(ModelView(ServiceEvent, db.session))
admin.add_view(ModelView(ServiceStaffConnect, db.session))


