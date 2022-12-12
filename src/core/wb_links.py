WB_PRODUCT_JSON_CARD_URL = 'https://card.wb.ru/cards/detail?nm=%s'

WB_GEO_PARAMS_URL = 'https://www.wildberries.ru/webapi/geo/saveprefereduserloc'

WB_PRODUCTS_PAGINATION_URL = 'https://search.wb.ru/exactmatch/ru/common/v4/search'     # noqa

WB_PRODUCTS_AMOUNT_BY_QUERY_URL = 'https://search.wb.ru/exactmatch/ru/male/v4/search'  # noqa

WB_PARAMS_FOR_URL = """?
appType=1&
couponsGeo={couponsGeo}&
curr=rub&
dest={dest}&
emp=0&
lang=ru&
locale=ru&
pricemarginCoeff=1.0&
query={query}&
reg=0&
regions={regions}&
resultset={resultset}&
spp=0&
suppressSpellcheck=false""".replace('\n', '')
