from asyncio import TimeoutError
from http import HTTPStatus
from http.cookies import SimpleCookie

from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ContentTypeError

from src.core.logging import logger


class MarketRequest:
    timeout = 3

    @classmethod
    async def __to_dict(cls, response: ClientResponse) -> dict | None:
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

        except ContentTypeError:
            logger.error('Failed to format: %s' % response.content_type)

    @classmethod
    async def GET(
        cls, url: str, as_dict: bool = True
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

        except (ClientConnectionError, TimeoutError) as err:
            logger.error('Connection %s to: % s' % (err, url))

    @classmethod
    async def POST(
        cls, url: str, as_dict: bool = True, **kw
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

        except (ClientConnectionError, TimeoutError) as err:
            logger.error('Connection %s to: % s' % (err, url))

    @classmethod
    async def cookies(
        cls, url: str, method: str, **kwargs
    ) -> SimpleCookie | dict:
        """Get only cookie from request to a remote server.

        #### Args:
        - url (str): A link to the resource.
        - method (str): Request method.
        - kw (dict): ...

        #### Returns:
        - SimpleCookie | dict: Empty dict if not cookie else SimpleCookie.
        """
        match method:
            case 'GET':
                request = cls.GET
            case 'POST':
                request = cls.POST
            case _:
                return {}

        response = await request(url=url, as_dict=False, **kwargs)
        return response.cookies
