import asyncio
import sys
import time
from pathlib import Path
from pprint import pprint
from typing import Any

root = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root))

from src.core.requestsing import MarketRequest
from src.markets.selen import Cooker
from src.settings import wb_config

PRODUCT_JSON_CARD = wb_config.PRODUCT_JSON_CARD
PAGINATION_PAGE = wb_config.PAGINATION_PAGE

class WbProduct:
    """A product from the market `Wildberries`.

    #### Example JSON:
    {
        'data': {
            'products': [
                {
                    'averagePrice': 0,
                    'brand': 'Heine',
                    'brandId': 423,
                    'colors': [
                        {
                            'id': 16777215,
                            'name': 'белый'
                        }
                    ],
                    'diffPrice': False,
                    'feedbacks': 0,
                    'id': 375,
                    'kindId': 2,
                    'name': 'Пуловер',
                    'pics': 1,
                    'priceU': 252000,
                    'promotions': [],
                    'rating': 0,
                    'root': 60197,
                    'sale': 0,
                    'salePriceU': 252000,
                    'siteBrandId': 690,
                    'sizes': [
                        {
                            'name': '42',
                            'optionId': 141670,
                            'origName': '34',
                            'rank': 6401,
                            'sign': 'SQnbgvoN4u0Ei/U9P8cUef1DBXU=',
                            'stocks': []
                        },
                        {
                            'name': '44',
                            'optionId': 197135,
                            'origName': '36/38',
                            'rank': 6801,
                            'sign': '4pzLGvXOKGQLUnq9YpAjC01AlTU=',
                            'stocks': []
                        },
                        {
                            'name': '48',
                            'optionId': 317376,
                            'origName': '40/42',
                            'rank': 7601,
                            'sign': 'rFAYlnqLXy1UvXu/XTqJhMXKSm8=',
                            'stocks': []
                        },
                        {
                            'name': '52',
                            'optionId': 426231,
                            'origName': '44/46',
                            'rank': 8301,
                            'sign': 'Gr3bMOinAVBy8ZQIoaTwyeQ+wT4=',
                            'stocks': []
                        }
                    ],
                    'subjectId': 160,
                    'subjectParentId': 1,
                    'supplierId': 128
                }
            ]
        },
    'params': {
        'curr': 'rub',
        'version': 1
    },
    'state': 0
    }
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
        data = await MarketRequest.GET(PRODUCT_JSON_CARD % self.id)
        if data:
            try:
                self.params = data['data']['products']
            except KeyError as err:
                print(err)

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

    @classmethod
    async def get_place_on_page(
        cls: 'WbProduct',
        product_id: int,
        query: str,
        sorting: str = 'popular',
        resultset: str = 'catalog'
    ) -> dict | int:
        """Get placement on the page.

        #### Args:
        - product_id: Product article.
        - query: Search query.
    
        #### Returns:
        - dict | int: Description of the position of the goods or
            the number of products viewed
        """
        page = 0
        amount = 0
        cooker = Cooker(cls.base_url)
        url = await cooker.update_url(PAGINATION_PAGE, query)

        while True:
            query_url = url + f'&{page=}' if page else url
            data = await MarketRequest.GET(url=query_url)
            
            try:
                data = data['data']['products']
            except (KeyError, TypeError) as err:
                print(err)
                return

            if not data:
                return amount

            for place, product in enumerate(data, 1):
                if product['id'] == product_id:
                    return {
                        'product_id': product_id,
                        'Название': product['name'],
                        'Начальная цена': product['priceU'] / 100,
                        'Цена продажи': product['salePriceU'] / 100,
                        'Страница': page + 1,
                        'Место': place,
                        'rank': (page + 1) * 100 + place
                    }
                # print(product['id'], product['name'])
                # print((page+1)*place)

            amount += len(data)
            page += 1


async def test():
    s = time.time()
    # p = WbProduct(124_256_512)
    # assert await p.get_product_name() == 'Конструктор в чупсе "Полиция"'
    # print('\nКлючевое слово: zarina')
    # print('ID Вашего продукта: 126022903')
    # d = await WbProduct.get_place_on_page(126022903, 'zarina')#, 'pricedown')
    # print(*d.items(), sep='\n')
    print('\nКлючевое слово: Омега 3')
    print('ID Вашего продукта: 37260674')
    d = await WbProduct.get_place_on_page(37260674, 'Омега 3', 'priceup')
    print(d, sep='\n')
    print('Время запроса: ', time.time() - s)


if __name__ == '__main__':
    # 37260674 Омега 3
    asyncio.run(test())
