import json
import asyncio
from typing import List
from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.repository_interface import RegisterRepositoryInterface
from telegram_bots.api.api import Api


class RegisterRepositoryRealisationDatabase(RegisterRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["CLIENT_URL"]
        self.api = Api()
    
    def __get_connection_data(self):
        with open('config.json', 'r') as f:
            connection_data = json.loads(f.read())
        return connection_data

    async def add_user(self, data: User):
        return self.api.post(url_path=self.url, data=data.json())
    
    async def get_user(self, tg_id: int, loop) -> User:
        response = asyncio.run_coroutine_threadsafe( self.api.get(url_path=self.url+'/info_client', params={'tg_id': tg_id}), loop)
        print(response)
        response = json.loads(response)

        if not 'message' in response:
            parsed = User(name=response[0]['name_client'], tg_id=response[0]['tg_id'], phone=response[0]['phone_num'])
            return parsed

    async def update_user(self, data: User):
        response = await self.api.put(url_path=self.url, data=data.json())
        return response
