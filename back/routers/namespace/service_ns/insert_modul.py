from models.all_models import MyService


def add_service(name_service: str, price: float):
    """Добавление новой услуги"""
    new_service = MyService(name_service, price)
    new_service.save_to_db()
