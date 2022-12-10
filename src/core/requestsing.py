import sys
from asyncio import TimeoutError
from http import HTTPStatus
from http.cookies import SimpleCookie

from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ContentTypeError

expected_errors = (
    ClientConnectionError, ContentTypeError, TimeoutError, TypeError
)


class MarketRequest:
    timeout = 3

    async def __to_dict(response: ClientResponse) -> dict | None:
        """Return responsse body as dict.

        #### Args:
        - response (ClientResponse): Response object.

        #### Returns:
        - dict | None: None if not body else dict.
        """
        try:
            response = await response.json(content_type=response.content_type)

            if not isinstance(response, dict):
                response = await response.json(content_type='text/plain')
            return response

        except ContentTypeError as err:
            print(err)
            return

    @classmethod
    async def GET(
        cls: 'MarketRequest', url: str, as_dict: bool = True
    ) -> ClientResponse | dict | None:
        """Execute an http `GET` request to a remote server.

        #### Args:
        - url (str): A link to the resource.
        - as_dict (bool): Return result as dict.

        #### Returns:
        - None: If the request is not successful.
        - dict | str: ...
        """
        try:
            async with ClientSession() as session:
                async with session.get(
                    url=url, timeout=cls.timeout
                ) as response:
                    if response.status != HTTPStatus.OK:
                        return
                    if as_dict:
                        return await cls.__to_dict(response)
                    return response

        except expected_errors as err:
            print(err)
            return

    @classmethod
    async def POST(
        cls: 'MarketRequest', url: str, as_dict: bool = True, **kw
    ) -> ClientResponse | dict | None:
        """Execute an http `POST` request to a remote server.

        #### Args:
        - url (str): A link to the resource.
        - as_dict (bool): Return result as dict.
        - kw (dict): ...

        #### Returns:
        - None: If the request is not successful.
        - dict | str: ...
        """
        try:
            async with ClientSession() as session:
                async with session.post(
                    url=url, timeout=cls.timeout, **kw
                ) as response:
                    if response.status != HTTPStatus.OK:
                        return
                    if as_dict:
                        return await cls.__to_dict(response)
                    return response

        except expected_errors as err:
            print(err)
            return
 
    @classmethod
    async def cookies(
        cls: 'MarketRequest', url: str, method: str, **kwargs
    ) -> SimpleCookie | dict:
        """Get only cookie from request to a remote server.

        #### Args:
        - url (str): A link to the resource.
        - method (str): Request method.
        - kw (dict): ...

        #### Returns:
        - SimpleCookie | dict: Empty dict if not cookie else SimpleCookie.
        """
        try:
            async with ClientSession() as session:
                match method:
                    case 'GET':
                        request = session.get
                    case 'POST':
                        request = session.post

                async with request(url=url, **kwargs) as response:
                    return response.cookies

        except expected_errors as err:
            print(err)
            return {}
    