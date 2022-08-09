from setting_web import db
from models.users_client.all_users_this_connecta import CompanyUsers

from api.api_client_company import _base_query


def update_data_client(tg_id, name=None, phone=None):
    client_data = _base_query()
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first()

    if name is not None:
        client_data.name_client = name
    if phone is not None:
        client_data.phone_num = phone
    db.session.commit()

