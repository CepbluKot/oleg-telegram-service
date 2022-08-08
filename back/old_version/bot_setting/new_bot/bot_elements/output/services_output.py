from bot_elements.getters.register_getters import register_data_get_phone_number, register_data_get_user_name


def output_chosen_service_data(service_name: str, service_week: str, service_day: str, user_id: str):
    """ Функция, получающая на вход данные о записи"""
    """ 
        service_name - Название услуги, service_week - неделя предоставления услуги, service_day - день услуги, user_id - айди пользователя;

        так же данные о пользователе: register_data_get_user_name(user_id) - его имя; register_data_get_phone_number(user_id) - его телефон; 
    """
    print(" Название услуги: ", service_name, " неделя предоставления услуги: ", service_week, " день услуги: ", service_day, " id изера: ", user_id, " имя юзера", register_data_get_user_name(user_id), " телефон ",  register_data_get_phone_number(user_id))
