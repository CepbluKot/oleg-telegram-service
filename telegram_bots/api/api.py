import aiohttp
import json
import asyncio
from aiohttp import ClientSession


class Api:
    def __init__(self) -> None:
        self.__session = None
        self.__connection_data = self.__get_connection_data()
        self.__base_url = self.__connection_data['API_URL']

        
    async def connect(self) -> None:
        if self.__session is not None:
            raise Exception(
                "You are trying to override an unclosed client session"
            )

        session_args = {'X-API-KEY': self.__connection_data['API_KEY']}
        self.__session = ClientSession(headers=session_args)


    def __get_connection_data(self):
        with open('../config.json', 'r') as f:
            connection_data = json.loads(f.read())

        return connection_data


    async def get(self, url_path: str):
        url = self.__base_url + url_path
        output = await self.__session.get(url)
        print('and')
        return output
