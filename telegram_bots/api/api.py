import aiohttp
import json
import asyncio
from aiohttp import ClientSession


class Api:
    def __init__(self) -> None:
        self.__connection_data = self.__get_connection_data()
        self.__base_url = self.__connection_data['API_URL']
        
        post_session_args = {'X-API-KEY': self.__connection_data['API_KEY'], 'Content-Type': 'application/json'}
        get_session_args = {'X-API-KEY': self.__connection_data['API_KEY']}
        put_session_args = {'X-API-KEY': self.__connection_data['API_KEY'], 'Content-Type': 'application/json'}
        delete_session_args = {'X-API-KEY': self.__connection_data['API_KEY'], 'Content-Type': 'application/json'}
        
        self.__post_session = ClientSession(headers=post_session_args)
        self.__get_session = ClientSession(headers=get_session_args)
        self.__put_session = ClientSession(headers=put_session_args)
        self.__delete_session = ClientSession(headers=delete_session_args)

    def __get_connection_data(self):
        with open('config.json', 'r') as f:
            connection_data = json.loads(f.read())

        return connection_data


    async def get(self, url_path: str, params=None):
        url = self.__base_url + url_path
        async with self.__get_session.get(url, params=params) as output:
            text = await output.text()
            text = json.loads(text)
            return text

    async def post(self, url_path: str, data):
        url = self.__base_url + url_path
        async with self.__post_session.post(url=url, data=data) as output:
            text = await output.text()
            text = json.loads(text)
            return text

    async def put(self, url_path: str, data):
        url = self.__base_url + url_path
        async with self.__put_session.put(url=url, data=data) as output:
            text = await output.text()
            text = json.loads(text)
            return text


    async def delete(self, url_path: str, data):
        url = self.__base_url + url_path
        async with self.__delete_session.delete(url=url, data=data) as output:
            text = await output.text()
            text = json.loads(text)
            return text
