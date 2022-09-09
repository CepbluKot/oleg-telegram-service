from setting_web import db
from models.service.service_connecta import MyService

from api.api_services import _base_query


def update_service(old_name, new_name=None, new_price=None):
    service = _base_query().filter(MyService.name_service == old_name)

    if new_name is not None:
        service.name_service = new_name

    if new_price is not None:
        service.price_service = new_price
    db.session.commit()
