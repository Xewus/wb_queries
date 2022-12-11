ERROR = """Что-то пошло не так..."""

ERROR_QUERY = """Неправильный запрос."""

START = """Привет!"""

DESCRIPTION = """
Этот бот позволяет проверить местоположение Вашего товара в выдаче \
маркетплейса `Wildberries` по различным поисковым запросам.
"""

CANCEL = """Предыдущие действия отменены."""

DEFAULT = """Извини, мои возможности ограничены.

Я занимаюсь только поиском.
"""

INPUT_ARTICLE = """Введите артикул."""

INPUT_QUERY = """Введите поисковый запрос."""

INPUT_ADDRESS = """Укажите город.

Примечания:
При вводе некорректного адреса в запросе будет установлен ДС.

Положение товара в выдаче немного меняется в зависимости от \
пространственно-временных координат запроса.
"""

ALL_DATA = """Идёт поиск по данным:

Артикул: %d
Поисковый апрос: %s
Адрес: %s
"""

NOT_EXIST = """Товар не найден."""

ANSWER_WITH_DATA = """
Двнный товар находится на странице: {page}.
Номер карточки на странице: {place}.
Положение среди всех товаров: {rank}.
"""

ANSWER_NOT_FOUND = """
По запросу `%s` найдено товаров: %s
Артикул `%s` среди них не обнаружен.
Либо ошибка соединения с Wildberries.
"""
