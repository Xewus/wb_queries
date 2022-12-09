from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())

chrome_options = None
# chrome_options = Options()
# chrome_options.add_argument("--headless")


class Cooker:
    """Get cookies and use they.

    #### Attrs:
    - url (str): A website that has cookies.
    - driver (selenium.webdriver.chrome.webdriver.WebDriver):
        Imitation of the `Chrome` browser.
    """
    def __init__(self, url: str) -> None:
        self.url = url
        self.driver = webdriver.Chrome(
            service=service, chrome_options=chrome_options
        )

    async def __get_wb_cookies(self) -> dict:
        """Get cookies from a site.

        #### Args:
        - url (str): A website address.

        #### Returns:
        - dict: [str, str]

        #### Example incoming cookies:
        - expires:
            Basket / User: 1 year.
            Geo: 1 yaer.
            Cache: 1 hour.
        - [
            {
                'domain': '.wildberries.ru',
                'expiry': 1670571617,
                'httpOnly': True,
                'name': '___wbs',
                'path': '/',
                'secure': False,
                'value': '25e54881-07f6-4bf6-93d1-537d5b023301.1670567417'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1705127417,
                'httpOnly': True,
                'name': '___wbu',
                'path': '/',
                'secure': False,
                'value': 574bb47f-facf-4b59-85d1-e43151598107.1670567417'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__tm',
                'path': '/',
                'secure': False,
                'value': '1670578217'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1702103417,
                'httpOnly': False,
                'name': 'BasketUID',
                'path': '/',
                'secure': False,
                'value': '72a91503-fd87-48e2-8c72-b19867129ee4'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': True,
                'name': '__pricemargin',
                'path': '/',
                'secure': False,
                'value': '1.0--'
            },
            {
                'domain': 'www.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': True,
                'name': 'ncache',
                'path': '/',
                'secure': False,
                'value': '159402_2737_117501_507_3158_120762_204939_117986_130744_1733_686_1193_206968_206348_205228_172430_117442_117866%3B80_64_83_4_38_33_70_82_69_68_86_30_40_48_1_22_66_31%3B1.0--%3B12_7_3_6_5_18_21%3B4%3B-1216601_-337422_-1114902_-1198055'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__sppfix',
                'path': '/',
                'secure': False,
                'value': '4'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__region',
                'path': '/',
                'secure': False,
                'value': '80_64_83_4_38_33_70_82_69_68_86_30_40_48_1_22_66_31'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__dst',
                'path': '/',
                'secure': False,
                'value': '-1216601_-337422_-1114902_-1198055'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__wbl',
                'path': '/',
                'secure': False,
                'value': 'cityId=0&regionId=0&city=Санкт-Петербург&phone=84957755505&latitude=59,939037&longitude=30,315784&src=1'
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__cpns',
                'path': '/',
                'secure': False,
                'value': '12_7_3_6_5_18_21'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1671172217,
                'httpOnly': False,
                'name': '__store',
                'path': '/',
                'secure': False,
                'value': '159402_2737_117501_507_3158_120762_204939_117986_130744_1733_686_1193_206968_206348_205228_172430_117442_117866'
            },
            {
                'domain': '.wildberries.ru',
                'expiry': 1702103417,
                'httpOnly': False,
                'name': '_wbauid',
                'path': '/',
                'secure': False,
                'value': '9810284461670567417'
            },
            {
                'domain': 'www.wildberries.ru',
                'httpOnly': False,
                'name': '__wba_s',
                'path': '/',
                'secure': False,
                'value': '1'
            }
        ]
        """
        self.driver.get(self.url)
        cookies = self.driver.get_cookies()
        self.driver.quit()
        cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies

    async def update_url(self, url: str, query: str) -> str | None:
        """Change the URL corresponding to the cookies and query.

        #### Args:
        - url (str): URL to change.
        - queries (str): Search query.

        #### Returns:
        - str: Changed URL.
        """
        try:
            cookies = await self.__get_wb_cookies()
        except WebDriverException as exc:
            print(exc)
            return

        query_keys = {
            'appType': 1,
            'couponsGeo': '12,7,3,6,5,18,21',
            'curr': 'rub',
            'dest': '-1216601,-337422,-1114902,-1198055,-0000',
            'emp': 0,
            'lang': 'ru',
            'locale': 'ru',
            'pricemarginCoeff': 1.0,
            'query': query,
            'reg': 0,
            'regions': '80,64,83,4,38,33,70,82,69,68,86,30,40,48,1,22,66,31',
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': 0,
            'suppressSpellcheck': 'false'
        }
        relevant_keys = {
            '__dst': 'dest',
            '__region': 'regions',
            '__cpns': 'couponsGeo',
            '__pricemargin': 'pricemarginCoeff',
        }

        for cookie_key in cookies.keys():
            key = relevant_keys.get(cookie_key, None)
            if key is not None:
                value = cookies[cookie_key].strip('_ —-')
                if key in {'dest', 'couponsGeo', 'regions'}:
                    value = ','.join(cookies[cookie_key].split('_'))
                query_keys[key] = value

        return url.format_map(query_keys)
