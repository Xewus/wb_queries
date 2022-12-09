import socket
from functools import cache
from pprint import pprint
from time import sleep
from urllib.parse import unquote

from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@cache
async def get_geo_coord(geoname: str | None = None) -> tuple[float, float]:
    default_lat = 55.7504461   # Moscow city
    default_long = 37.6174943
    if geoname:
        geoname += ', RU'
        geo_loc = Nominatim(user_agent='GetLoc')
        location = geo_loc.geocode(query=geoname)
        if location:
            return location.latitude, location.longitude

    return default_lat, default_long


async def get_wb_cookies(url: str, geoname: str | None = None) -> dict:
    """Get cookies from a site.

    #### Args:
    - url (str): A website address.

    #### Returns:
    - dict: {name: value}

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
    geo_lat, geo_long = await get_geo_coord(geoname)

    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()

    PROXY="176.9.119.170:8080"


    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",

    }
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": geo_lat,
            "longitude": geo_long,
            "accuracy": 100
    })
    driver.get(url)
    sleep(1)
    cookies = driver.get_cookies()
    driver.quit()
    cookies = {cookie['name']: cookie['value'] for cookie in cookies}
    print(unquote(cookies['__wbl']), cookies['__dst'], cookies['__region'], sep='\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()
    return cookies
