import asyncio
import sys
from math import ceil
from pathlib import Path
from typing import Any

root = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root))

from src.core.logging import logger  # noqa
from src.core.requestsing import MarketRequest  # noqa
from src.core.utils import get_params_for_url  # noqa
from src.core.wb_links import WB_PRODUCT_JSON_CARD_URL  # noqa
from src.core.wb_links import WB_PRODUCTS_AMOUNT_BY_QUERY_URL  # noqa
from src.core.wb_links import WB_PRODUCTS_PAGINATION_URL  # noqa


class WbProduct:
    """A product from the market `Wildberries`.
    """
    base_url = 'https://www.wildberries.ru/'

    def __init__(self, id: int | str) -> None:
        if isinstance(id, str) and not id.isdecimal():
            raise ValueError('`~id %s` is not a number')
        self.id = id

    async def __set_params(self) -> None:
        """Get the product params from a remote server and set into parameter.
        """
        self.params = []
        data = await MarketRequest.GET(WB_PRODUCT_JSON_CARD_URL % self.id)
        if data:
            try:
                self.params = data['data']['products']
            except KeyError:
                logger.error('Error with article: %d' % self.id)

    async def __get_product_param(self, key: str) -> Any | None:
        """Get the product parameter.

        #### Args:
        - keys (str): Names of fields to search for data.

        #### Returns:
        - None: If the parameter is missing.
        - Any: The parametr value.
        """
        if getattr(self, 'product', None) is None:
            await self.__set_params()
        for param in self.params:
            if isinstance(param, dict) and param.get(key, None):
                return param[key]

    async def get_param(self, key: str) -> Any | None:
        """Get the product parameter.

        #### Args:
        - keys (str): Names of fields to search for data.

        #### Returns:
        - None: If the parameter is missing.
        - Any: The parametr value.
        """
        return await self.__get_product_param(key)

    async def get_product_name(self) -> str | None:
        """Get the product name.

        #### Returns:
        - None: If the parameter is missing.
        - str: The product name.
        """
        return await self.__get_product_param('name')

    @staticmethod
    async def get_amount_by_query(query: str, address: str) -> int:
        """Get the number of products according to the specified query.

        #### Args:
        - query (str): Search query.
        - address (str): Address to search for.

        #### Returns:
        - int: Amount of products per search query.
        """
        url_params, _ = await get_params_for_url(
            query,
            resultset='filters',
            address=address
        )
        url = WB_PRODUCTS_AMOUNT_BY_QUERY_URL + url_params
        data = await MarketRequest.GET(url)

        try:
            return data['data']['total']
        except (KeyError, TypeError):
            logger.error('Incorrect response for: %s' % url)
            return 0

    async def __find_place(self, url, page: int, dataset: list) -> None:
        """Find the product on the page.

        #### Args:
        - url (str): URL of the page to search for.
        - page (int): Page number.
        - dataset (list): List with results.
        """
        data = await MarketRequest.GET(url)

        try:
            data = data['data']['products']
        except (KeyError, TypeError):
            logger.error('Incorrect response for: %s' % url)
            return

        for place, product in enumerate(data, 1):
            if product['id'] == self.id:
                dataset[page] = place
                return

    async def get_place_on_page(
        self,
        query: str,
        sort: str = 'popular',
        resultset: str = 'catalog',
        address: str = 'Москва'
    ) -> dict[str, int]:
        """Get placement on the page.

        #### Args:
        - query: Search query.
        - sort (str): Sorting products.
        - resultset (str): Type of returned JSON.
        - address (str): Address to search for.

        #### Returns:
        - dict[str, int]: Description of the position of the product.
        """
        await logger.info(
            'Got request with article: %d, query: %s, address: %s' % (
                self.id, query, address
            )
        )
        amount = await self.get_amount_by_query(query, address)
        last_page = min(ceil(amount // 100), 60)
        url_params, address = await get_params_for_url(
            query, sort, resultset, address
        )
        url = WB_PRODUCTS_PAGINATION_URL + url_params
        dataset = [None] * last_page
        tasks = [None] * last_page
        result = {
            'amount': amount,
            'page': 0,
            'place': 0,
            'rank': 0
        }

        for page in range(1, last_page + 1):
            query_url = url + f'&{page=}' if page > 1 else url
            tasks[page - 1] = asyncio.create_task(
                self.__find_place(query_url, page - 1, dataset)
            )

        await asyncio.gather(*tasks)

        for page, place in enumerate(dataset, 1):
            if place:
                result['page'] = page
                result['place'] = place
                result['rank'] = (page - 1) * 100 + place
                break

        return result


async def test():
    p = WbProduct(124_256_512)
    assert await p.get_product_name() == 'Конструктор в чупсе "Полиция"'

    print('\nКлючевое слово: zarina')
    print('ID продукта: 126022903')
    d = await WbProduct(
        126022903
    ).get_place_on_page('zarina', sort='pricedown')
    print(*d.items(), sep='\n')

    print('\nКлючевое слово: Омега 3')
    print('ID продукта: 37260674')
    d = await WbProduct(
        37260674
    ).get_place_on_page('Омега 3', address='Питер')
    print(*d.items(), sep='\n')


if __name__ == '__main__':
    asyncio.run(test())
