from models.all_models import CompanyUsers, AllBooking

from .schema import InfoUsersComSchema
from .validate import FilterClient as Filter


def _base_query():
    client = CompanyUsers.query
    return client


def _base_query_booking():
    client_booking = AllBooking.query
    return client_booking


def all_client():
    all_client_data = _base_query()
    api_all_client_schema = InfoUsersComSchema(many=True)
    return api_all_client_schema.dump(all_client_data)


def get_filter_client(filter_cl: Filter):
    client_data = _base_query()

    if filter_cl.tg_id is not None and len(filter_cl.tg_id) > 0:
        client_data = client_data.filter(CompanyUsers.tg_id == filter_cl.tg_id)

    if filter_cl.phone_num is not None and len(filter_cl.phone_num) > 0:
        client_data = client_data.filter(CompanyUsers.phone_num == filter_cl.phone_num)

    if (filter_cl.name is not None) and (filter_cl.tg_id is not None or filter_cl.phone_num is not None) \
            and len(filter_cl.name) > 0:
        client_data = client_data.filter(CompanyUsers.name_client == filter_cl.name)

    api_client_schema = InfoUsersComSchema()
    return api_client_schema.dump(client_data)


def check_exit_us(tg_id=None):
    client_data = _base_query()
    client_data = client_data.filter(CompanyUsers.tg_id == tg_id).first() is not None

    return client_data

