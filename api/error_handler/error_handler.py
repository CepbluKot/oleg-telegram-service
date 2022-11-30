from aiohttp.client_reqrep import ClientResponse
from requests import Response
from api.data_structures import ErrorType


def handle_error_async_api(response: ClientResponse, response_text: str):
    error_info = ErrorType()
    if response.status == 400:
        error_info.bad_request = True
        error_info.has_error = True

    if response.status == 404:
        error_info.not_found = True
        error_info.has_error = True

    if 'Please provide a valid mobile phone number' in response_text:
        error_info.wrong_phone_number = True
        error_info.has_error = True

    if response.status == 401:
        error_info.unauthorized = True
        error_info.has_error = True

    if 'this event alredy exist' in response_text:
        error_info.user_already_exists = True
        error_info.has_error = True

    if 'not find' in response_text:
        error_info.booking_doesnt_exist = True
        error_info.has_error = True

    return error_info

def handle_error_sync_api(response: Response):
    error_info = ErrorType()

    if response.status_code == 400:
        error_info.bad_request = True
        error_info.has_error = True

    if response.status_code == 404:
        error_info.not_found = True
        error_info.has_error = True

    if 'Please provide a valid mobile phone number' in response.text:
        error_info.wrong_phone_number = True
        error_info.has_error = True

    if response.status_code == 401:
        error_info.unauthorized = True
        error_info.has_error = True

    if 'this event alredy exist' in response.text:
        error_info.user_already_exists = True
        error_info.has_error = True

    return error_info
