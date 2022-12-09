PRODUCT_JSON_CARD='https://card.wb.ru/cards/detail?nm=%s'

PRODUCT_PAGE='https://www.wildberries.ru/catalog/%s/detail.aspx'

SEARCH_JSON='https://catalog-ads.wildberries.ru/api/v5/search?keyword=%s&sort=popular'

POINTS_OF_DELIVERY='https://static.wbstatic.net/data/all-poo-fr-v2.json'

PAGINATION_PAGE="""https://search.wb.ru/exactmatch/ru/common/v4/search?
appType=1&
curr=rub&
dest={dest}&
emp=0&
lang=ru&
locale=ru&
pricemarginCoeff=1.0&
query={query}&
reg=0&
regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&
resultset={resultset}&
sort={sort}&
spp=0&
suppressSpellcheck=false""".replace('\n', '')
