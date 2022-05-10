from setting_web import flask_app

import admin_tools

import api.api_booking
import api.api_services
import api.api_authentication
import api.api_client_company
import api.api_workig_date

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
