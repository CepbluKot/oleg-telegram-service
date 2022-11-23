from pydantic import BaseModel
from telegram_bots.modules.general_data_structures import GeneralDataStructure


class User(GeneralDataStructure):
    name: str = ''
    tg_id: int = -1
    phone: str = -1


class UserForParse(BaseModel):
    name: str
    tg_id: int
    phone: str
