import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import start_kb
from src.bot.texts import (TXT_ANSWER_NOT_FOUND, TXT_ANSWER_WITH_DATA,
                           TXT_ERROR, TXT_ERROR_QUERY, TXT_HELP,
                           TXT_INPUT_SEARCH, TXT_START)
from src.core.enums import CallBackData, Commands
from src.markets.wildberiies import WbProduct
from src.settings import bot_config

# bot_configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(
    token=bot_config.TOKEN.get_secret_value(),
    parse_mode='HTML'
)
disp = Dispatcher(bot)


@disp.callback_query_handler(lambda c: c.data == CallBackData.OFFCOURSE)
async def callback_of_course(query: CallbackQuery):
    await bot.answer_callback_query(query.id)
    await bot.send_message(
        query.from_user.id,
        text=TXT_INPUT_SEARCH
    )


@disp.message_handler(commands=[Commands.START])
async def start_command(message: Message):
    await message.answer(TXT_START, reply_markup=start_kb)


@disp.message_handler(commands=[Commands.HELP])
async def help_command(msg: Message):
    await msg.answer(TXT_HELP.format_map(Commands.as_dict()))


@disp.message_handler()
async def search_message(msg: Message):
    query = msg.text.split(maxsplit=1)
    if len(query) < 2 or not query[0].isnumeric():
        await msg.answer(TXT_ERROR_QUERY)
        return

    art, query = int(query[0]), query[1]
    wb_product = WbProduct(art)
    data = await wb_product.get_place_on_page(query)

    if isinstance(data, dict):
        text = TXT_ANSWER_WITH_DATA.format_map(data)
    elif isinstance(data, int):
        text = TXT_ANSWER_NOT_FOUND % (query, data, art)
    else:
        text = TXT_ERROR

    await msg.answer(text)


def run_bot():
    executor.start_polling(disp)
