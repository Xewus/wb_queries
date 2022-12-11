# wb_queries (test task)
Бот получает данные с маркетплейса **Wildberries**.
***
# Task
Написать телеграм бота, который принимает от пользователя поисковый запрос и номенклатуру(артикул товара),  в ответ получает сообщение. Бот парсит данные с www.wildberries.ru. Если товар находится на первых 100 страницах поиска, присылаете сообщение с номером страницы и позиции, если нет, то любое текстовое сообщение. 

Стек: Python(3.9 и выше), aiogram, aiohttp/requests, docker(по желанию)

Дополнительные задания:
1) Добавить получение результатов в зависимости от пункта выдачи заказов клиента.

Пример сообщения пользователя:

37260674 Омега 3
***
### Инструкция по использованию

1. Если у Вас есть **Docker**.

Скачать и запустить образ (172 МВ):
```
sudo docker run -e "BOT_TOKEN=<Токен Вашего бота>
```
2.
Создать директорию для приложения и перейти в неё:
```
mkdir wb_bot && cd wb_bot
```
Скачать код с Githab:
```
git@github.com:Xewus/wb_queries.git
```
Переименовать файд `.env.example` в `.env` и вписать в него нужные данные.

Установить зависимости:
```
pip3 install -U pip && pip install -r /app/requirements.txt --no-cache-dir
```
Запустить бота:
```
python3 start_app.py
```