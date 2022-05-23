from setting_web import flask_app

import routers.admin_tools
#import routers.router_booking
import routers.router_services
import routers.routers_client_company
import routers.routers_working_date
import api.api_authentication

import bissnes_logic.insert_data_modul

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
