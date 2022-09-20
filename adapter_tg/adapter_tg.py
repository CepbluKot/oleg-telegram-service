import requests
import rapidjson

type_connect = 'http'
ip = '127.0.0.1'
port = '8001'


def get_all_users():
    requests_str = type_connect + '://' + ip + ':' + port + '/api_booking/client'

    try:
        # example: [{'name_client': 'OLEG', 'tg_id': 12232, 'phone_num': '111', 'id': 1}]
        return requests.get(requests_str).json(), 200
    except:
        return None, 404


def change_users(tg_id: int, new_name: str = None, new_phone: str = None):
    requests_str = type_connect + '://' + ip + ':' + port + '/api_booking/client'
    new_data = {"tg_id": tg_id, "phone": new_phone, "name": new_name}

    try:
        return requests.put(requests_str, json=new_data).json(), 200
    except:
        return None, 404


def find_users(tg_id: int):
    requests_str = type_connect + '://' + ip + ':' + port + '/api_booking/client/int:' + str(tg_id)

    try:
        # example ([{'id': 1, 'name_client': 'oleg', 'tg_id': 12232, 'phone_num': '1111111'}], 200)
        return requests.get(requests_str).json(), 200
    except:
        return None, 404
