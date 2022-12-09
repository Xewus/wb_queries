import sys
from asyncio import TimeoutError
from http import HTTPStatus
from pathlib import Path

import aiohttp
from aiohttp import ClientResponse
from aiohttp.client_exceptions import ClientConnectionError, ContentTypeError

root = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root))


class MarketRequest:
    timeout = 3

    async def __to_dict(response: ClientResponse) -> dict | None:
        try:
            response = await response.json(content_type=response.content_type)

            if not isinstance(response, dict):
                response = await response.json(content_type='text/plain')
            return response

        except ContentTypeError as err:
            print(err)
            return

    @classmethod
    async def __request_get(cls: 'MarketRequest', url: str) -> dict | None:
        """Execute an http request to a remote server.

        #### Args:
        - url (str): A link to the resource.
        - content (str): The desired format of the returned data.
                            One of [`dict`, `str`]

        #### Returns:
        - None: If the request is successful.
        - dict | str: ...
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url, timeout=cls.timeout
                ) as response:
                    if response.status != HTTPStatus.OK:
                        return
                    return await cls.__to_dict(response)

        except (ClientConnectionError, TimeoutError) as err:
            print(err)
            return

    @classmethod
    async def __request_post(
        cls: 'MarketRequest', url: str, data: dict
    ) -> dict | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url, data=data, timeout=cls.timeout
                ) as response:
                    if response.status != HTTPStatus.OK:
                        return
                    return await cls.__to_dict(response)

        except (ClientConnectionError, ContentTypeError, TimeoutError) as err:
            print(err)
            return

    @classmethod
    async def GET(cls: 'MarketRequest', url: str) -> dict | None:
        return await cls.__request_get(url)

    @classmethod
    async def POST(
        cls: 'MarketRequest', url: str, data: dict = None
    ) -> dict | None:
        return await cls.__request_post(url, data)
