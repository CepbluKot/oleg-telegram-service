import json
from pydantic import BaseModel
from aiohttp.client_reqrep import ClientResponse
from requests import Response

from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.api_repository.repository_interface import (
    RegisterRepositoryInterface,
)

from api.api import ApiAsync, ApiSync
from api.data_structures import ApiOutput, ErrorType
from api.error_handler.error_handler import handle_error_async_api, handle_error_sync_api


class RegisterRepositoryRealisationDatabaseAsync(RegisterRepositoryInterface):
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


    async def __error_checker(self, response: ClientResponse):
        response_text = await response.text()

        if response:
            return handle_error_async_api(response=response, response_text=response_text)

        elif not response:
            return ErrorType(timeout=True, has_error=True)


    async def get_user(self, tg_id: int) -> User:
        try:
            api = ApiAsync()
            response = await api.get(
                url_path=self.url + "/info_client", params={"tg_id": tg_id}
            )
            error_check = await self.__error_checker(response)

            # if not self.__is_exception(response=response):
            #     response = json.loads(response)
            #     parsed = UserForParse.parse_raw(response[0])
            #     output = User(name=parsed.name, tg_id=parsed.tg_id, phone=parsed.phone)
            output = User()
            # else:
            #     output = User(is_exception=True, exception_data=str(response))
            #     print('output',output)
            
            return ApiOutput(data=output, errors=error_check)
        except:
            print("error - get_user")

    async def update_user(self, data: User) -> User:
        try:
            api = ApiAsync()
            response = await api.put(url_path=self.url, data=data.json())
            response = json.loads(response)
            if not self.__is_exception(response):
                print('resp', response)
                # parse = UserForParse.parse_raw(response[0])
                output = User(tg_id=response['tg_id'])
            else:
                output = User(is_exception=True, exception_data=str(response))
        
            return ApiOutput(data=output, errors=error_check)
        except:
            print("error - update_user")

    async def register_user(self, data: User) -> User:
        try:
            api = ApiAsync()
            response = await api.post(url_path=self.url, data=data.json())
            response = json.loads(response)

            error_check = await self.__error_checker(response)
            if not error_check.has_error:
                
                print('resp', response)
               
                output = User(tg_id=response['tg_id'], phone=response['phone'], name=response['name'])
            else:
                output = User(is_exception=True, exception_data=str(response))
        
            return ApiOutput(data=output, errors=error_check)
        except:
            print("error - update_user")


class RegisterRepositoryRealisationDatabaseSync(RegisterRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["CLIENT_URL"]
        self.api = ApiSync()

    def __get_connection_data(self):
        try:
            with open("config.json", "r") as f:
                connection_data = json.loads(f.read())
            return connection_data
        except:
            print("error - __get_connection_data")

    def __error_checker(self, response: Response):
        response_text = response.text

        if response:
            return handle_error_sync_api(response=response, response_text=response_text)

        elif not response:
            return ErrorType(timeout=True, has_error=True)


    def get_user(self, tg_id: int) -> User:
        try:
            
            response = self.api.get(
                url_path=self.url + "/info_client", params={"tg_id": tg_id}
            )
            error_check = self.__error_checker(response)
            # if not self.__is_exception(response=response):
            #     response = json.loads(response)
            #     parsed = UserForParse.parse_raw(response[0])
            #     output = User(name=parsed.name, tg_id=parsed.tg_id, phone=parsed.phone)
            output = User()
            # else:
            #     output = User(is_exception=True, exception_data=str(response))
            #     print('output',output)
            
            return ApiOutput(data=output, errors=error_check)

        except:
            print("error - get_user")

    def update_user(self, data: User) -> User:
        try:
            response = self.api.put(url_path=self.url, data=data.json())
            response = json.loads(response)
            
            error_check = self.__error_checker(response)
            if not error_check.has_error:
                print('resp', response)
                # parse = UserForParse.parse_raw(response[0])
                output = User(tg_id=response['tg_id'], phone=response['phone'], name=response['name'])
            else:
                output = User(is_exception=True, exception_data=str(response))
        
            return ApiOutput(data=output, errors=error_check)
        except:
            print("error - update_user")


    def register_user(self, data: User) -> User:
        try:
            response = self.api.post(url_path=self.url, data=data.json())
            response = json.loads(response)

            error_check = self.__error_checker(response)
            if not error_check.has_error:    
                print('resp', response)
                output = User(tg_id=response['tg_id'], phone=response['phone'], name=response['name'])
            else:
                output = User(is_exception=True, exception_data=str(response))
        
            return ApiOutput(data=output, errors=error_check)
        except:
            print("error - update_user")
