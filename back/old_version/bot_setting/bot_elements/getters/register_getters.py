from bots_setting.bot_elements.storages.register_storages import register_data
from queries.queries_client_company import get_filter_client, check_exit_us


def register_data_get():
    """ (Для БД) возвращает registerData"""
    """ 
        Пример registerData:
    {'user_name': user_name, 'phone_number': phone_number}
    """
    return register_data


def register_data_get_user_name(user_id: int):
    """ (Для БД) Возвращает имя юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'user_name': user_name, 'phone_number': phone_number}
    """
    #return register_data[user_id]['user_name']
    return get_filter_client(tg_id=user_id)['name_client']

def register_data_get_phone_number(user_id: int):
    """ (Для БД) Возвращает номер телефона юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'user_name': user_name, 'phone_number': phone_number}
    """
    #return register_data[user_id]['phone_number']
    return get_filter_client(user_id)['phone_num']

def register_data_check_is_registered(user_id: int):
    """ (Для БД) Проверяет есть ли юзер в registerData"""
    """ 
        Формат registerData:
        {user_id: {'user_name': user_name, 'phone_number': phone_number}, ...}
    """
    #return user_id in register_data.keys()
    return check_exit_us(user_id)
