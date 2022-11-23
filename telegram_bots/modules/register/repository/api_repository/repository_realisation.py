import json
from pydantic import BaseModel
from telegram_bots.modules.register.data_structures import User, UserForParse
from telegram_bots.modules.register.repository.api_repository.repository_interface import (
    RegisterRepositoryInterface,
)
from api.api import Api


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
        if response:
            if "message" in response or 'internal' in response:
                return True

    async def get_user(self, tg_id: int) -> User:
        try:
            api = Api()
            response = await api.get(
                url_path=self.url + "/info_client", params={"tg_id": tg_id}
            )
            
            if not self.__is_exception(response=response):
                response = json.loads(response)
                parsed = UserForParse.parse_raw(response[0])
                output = User(name=parsed.name, tg_id=parsed.tg_id, phone=parsed.phone)
                
            else:
                output = User(is_exception=True, exception_data=str(response))
                print('output',output)
            
            return output

        except:
            print("error - get_user")

    async def update_user(self, data: User) -> User:
        try:
            api = Api()
            response = await api.put(url_path=self.url, data=data.json())
            response = json.loads(response)
            if not self.__is_exception(response):
                print('resp', response)
                # parse = UserForParse.parse_raw(response[0])
                output = User(tg_id=response['tg_id'], phone=response['phone'], name=response['name'])
            else:
                output = User(is_exception=True, exception_data=str(response))
        
            return output
        except:
            print("error - update_user")
