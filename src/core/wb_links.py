PRODUCT_JSON_CARD = 'https://card.wb.ru/cards/detail?nm=%s'

GEO_PARAMS = 'https://www.wildberries.ru/webapi/geo/saveprefereduserloc'

PAGINATION_PAGE = """https://search.wb.ru/exactmatch/ru/common/v4/search?
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
sort={sort}&
spp=0&
suppressSpellcheck=false""".replace('\n', '')
