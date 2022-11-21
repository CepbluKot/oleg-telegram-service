import json
from telegram_bots.modules.general_data_structures import Data
from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.repository_interface import (
    RegisterRepositoryInterface,
)
from telegram_bots.api.api import Api


class RegisterRepositoryRealisationDatabase(RegisterRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["CLIENT_URL"]

    def __get_connection_data(self):
        try:
            with open("config.json", "r") as f:
                connection_data = json.loads(f.read())
            return connection_data
        except:
            print("error - __get_connection_data")

    def __is_exception(self, response: dict):
        if "message" in response or 'internal' in response:
            return True

    async def get_user(self, tg_id: int) -> Data:
        try:
            api = Api()
            response = await api.get(
                url_path=self.url + "/info_client", params={"tg_id": tg_id}
            )
            
            if not self.__is_exception(response=response):
                response = json.loads(response)
                parsed = User.parse_raw(response[0])
       
                output = Data(data=parsed)  
            else:
                output = Data(is_exception=True, exception_data=response)
            
            return output

        except:
            print("error - get_user")

    async def update_user(self, data: User) -> Data:
        try:
            api = Api()
            response = await api.put(url_path=self.url, data=data.json())
            response = json.loads(response)
            if not self.__is_exception(response):
                print('resp', response)
                parse = User.parse_raw(response[0])
                output = Data(data=response)
            else:
                output = Data(is_exception=True, exception_data=response)
        
            return output
        except:
            print("error - update_user")
