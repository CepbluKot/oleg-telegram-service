import requests
from config_adapter_tg import cfg_connect as config

type_connect = 'http'
ip = '127.0.0.1'
port = '5000'


def default_router():
    return config.type_connect + '://' + config.ip_adr + ':' + config.port + '/'


#поиск свободного окна для записи
def search_window(name_service: str):
    requests_str = default_router() + 'api_booking/booking/search'
    new_data = {"name_service": name_service}

    try:
        return requests.post(requests_str, json=new_data).json(), 200
        # answer_xample = https://codeshare.io/K8DWDM
    except:
        return None, 404


def all_service():
    requests_str = default_router() + 'api_booking/service'
    #[{'duration': '01:00:00', 'max_booking': 1, 'price_service': 222.0, 'id': 2, 'name_service': 'chistka'}]
    try:
        return requests.get(requests_str).json(), 200
    except:
        return None, 404


def add_client(tg_id: int, new_name: str, new_phone: str):
    requests_str = default_router() + 'api_booking/client'
    new_data = {"tg_id": tg_id, "phone": new_phone, "name": new_name}

    try:
        return requests.post(requests_str, json=new_data).json(), 200
    except:
        return None, 404


def add_client(tg_id: int, new_name: str, new_phone: str):
    requests_str = default_router() + 'api_booking/client'
    new_data = {"tg_id": tg_id, "phone": new_phone, "name": new_name}

    try:
        return requests.post(requests_str, json=new_data).json(), 200
    except:
        return None, 404


def get_all_users():
    requests_str = default_router() + 'api_booking/client'

    try:
        # example: [{'name_client': 'OLEG', 'tg_id': 12232, 'phone_num': '111', 'id': 1}]
        return requests.get(requests_str).json(), 200
    except:
        return None, 404


def change_users(tg_id: int, new_name: str = None, new_phone: str = None):
    requests_str = default_router() + 'api_booking/client'
    new_data = {"tg_id": tg_id, "phone": new_phone, "name": new_name}

    try:
        return requests.put(requests_str, json=new_data).json(), 200
    except:
        return None, 404


def find_users(tg_id: int):
    requests_str = default_router() + 'api_booking/client/int:' + str(tg_id)

    try:
        # example ([{'id': 1, 'name_client': 'oleg', 'tg_id': 12232, 'phone_num': '1111111'}], 200)
        return requests.get(requests_str).json(), 200
    except:
        return None, 404
