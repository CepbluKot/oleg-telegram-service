from bots_setting.bot_elements.getters.register_getters import register_data_get_phone_number, register_data_get_user_name
from bots_setting.bot_elements.storages.register_storages import register_data

from bissnes_logic.insert_data_modul import add_new_us
from bissnes_logic.update_data.update_client import update_data_client


async def register_data_add_user(user_id: int, user_name: str, phone_number: str):
    """ (Для БД) Добавляет рег. данные пользователя"""
    """
        user_id -айди пользователя, user_name - имя пользователя, phone_number - номер телефона
    """
    """ 
        Пример registerData:
    {'user_name': user_name, 'phone_number': phone_number}
    """
    #register_data[user_id] = {'user_name': user_name, 'phone_number': phone_number}
    add_new_us(user_id, user_name, phone_number)


def register_data_change_user_name(user_id: int, new_user_name: str):
    """ (Для БД) Изменяет рег. данные пользователя"""
    """
        user_id -айди пользователя, chosen_fio - фио пользователя, chosen_group - группа, chosen_role - роль
    """
    """
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """
    #register_data[user_id] = {'user_name': new_user_name, 'phone_number': register_data_get_phone_number(user_id)}
    update_data_client(user_id, name=new_user_name)

def register_data_change_phone_number(user_id: int, new_phone_number: str):
    """ (Для БД) Изменяет рег. данные пользователя"""
    """
        user_id -айди пользователя, chosen_fio - фио пользователя, chosen_group - группа, chosen_role - роль
    """
    """
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """
    #register_data[user_id] = {'user_name': register_data_get_user_name(user_id), 'phone_number': new_phone_number}
    update_data_client(user_id, phone=new_phone_number)