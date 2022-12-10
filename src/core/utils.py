from cache import AsyncLRU, AsyncTTL
from geopy.adapters import AioHTTPAdapter
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from src.core.requestsing import MarketRequest
from src.core.wb_links import GEO_PARAMS, PAGINATION_PAGE


@AsyncLRU(maxsize=128)
async def get_geo_coord(geoname) -> tuple[str, float, float]:
    """Get correct address, latitude, longitude.
    
    #### Args:
    - geoname (str): Name of geolocation.

    #### Returns:
    - tuple [str, float, float]: Correct address, latitude, longitude.
    """
    try:
        async with Nominatim(
            user_agent='GetLoc',
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            location = await geolocator.geocode(
                query=geoname, language='ru', country_codes='ru'
            )
            if location:
                return (
                    location.address,
                    location.latitude,
                    location.longitude
                )
    except GeocoderTimedOut:
        pass

    return 'Москва', 55.7504461, 37.6174943


@AsyncTTL(time_to_live=60 * 10, maxsize=128)
async def url_with_data(
    query: str, sorting: str, resultset: str, address: str
) -> tuple[str, str]:
    """Fill in the url with data.
    
    #### Args:
    - query (str): Search query.
    - sorting (str): Sorting products.
    - resultset (str): Type of returned JSON.
    - address (str): Address to search for.

    #### Returns:
    - tuple [str, str]: (URL, address). 
    """
    address, lat, long = await get_geo_coord(address)

    geo_data = {
        'address': address,
        'latitude': lat,
        'longitude': long,
    }
    headers = {'x-requested-with': 'XMLHttpRequest' }

    cookies = await MarketRequest.cookies(
        GEO_PARAMS, 'POST', headers=headers, data=geo_data
    )

    data_to_url = {
        'sort': sorting,
        'resultset': resultset,
        'query': query
    }

    for key, value in cookies.items():
        if key == '__dst':
            data_to_url['dest'] = ','.join(value.value.split('_'))
        if key == '__region':
            data_to_url['regions'] = ','.join(value.value.split('_'))
    
    return PAGINATION_PAGE.format_map(data_to_url), address
