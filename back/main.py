from setting_web import flask_app

import routers.admin_tools
import routers.router_booking
import routers.router_services
import routers.routers_client_company
import routers.routers_working_date
import api.api_authentication

import bissnes_logic.insert_data_modul


"""Добавление дня, предоставление записей на недели по одному дню, главная страница, продумать таблицу настроек(поля, типы данных), валидация"""
"""Продумать какое нужно апи для добавления новых дней(сделать проверку) и водавать предупреждения о том, что какие-то дни нужно перезаписать"""
"""Поэтапно расписать телегу (сообщения, и результат)"""
"""Написать обработчики ошибок"""

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
