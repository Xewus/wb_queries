import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import start_kb
from src.bot.states import UserState, storage
from src.bot.texts import (TXT_ANSWER_NOT_FOUND, TXT_ANSWER_WITH_DATA,
                           TXT_ERROR, TXT_ERROR_QUERY, TXT_HELP,
                           TXT_INPUT_SEARCH, TXT_START)
from src.core.enums import CallBackData, Commands
from src.core.utils import get_geo_coord
from src.markets.wildberiies import WbProduct
from src.settings import bot_config

# bot_configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=bot_config.TOKEN.get_secret_value(),
    parse_mode='HTML'
)
disp = Dispatcher(bot, storage=storage)



@disp.message_handler(commands=[Commands.SEARCH])
async def search_command(msg: Message):
    await msg.answer('Введите артикул')
    await UserState.article.set()

@disp.message_handler(state=UserState.article)
async def get_article(msg: Message, state: FSMContext):
    if not msg.text.isdecimal():
        await msg.answer(TXT_ERROR_QUERY)
        return await msg.answer('Введите артикул')
    
    article = int(msg.text)
    name = await WbProduct(article).get_product_name()

    if name is None:
        await state.finish()
        return await msg.answer(TXT_ANSWER_NOT_FOUND % ('', 0, msg.text))

    await state.update_data(article= article)
    await msg.answer(f"{name}\nОтлично! Теперь введите запрос.")
    await UserState.next()

@disp.message_handler(state=UserState.query)
async def get_article(msg: Message, state: FSMContext):
    await state.update_data(query = msg.text)
    await msg.answer("Отлично! Теперь введите ваш адрес.")
    await UserState.address.set()

@disp.message_handler(state=UserState.address)
async def get_article(msg: Message, state: FSMContext):
    address, *_ = await get_geo_coord(msg.text)
    await msg.answer(address)
    await state.update_data(address = msg.text)
    data = await state.get_data()

    await msg.answer(
        f'Артикул: {data["article"]}\n'
        f'Запрос: {data["query"]}\n'
        f'Адрес:  {address}'
    )

    result = await WbProduct(
        data['article']
    ).get_place_on_page(
        query=data['query'],
        address=data['address']
    )

    if isinstance(result, dict):
        text = TXT_ANSWER_WITH_DATA.format_map(result)
    elif isinstance(result, int):
        text = TXT_ANSWER_NOT_FOUND % (data['query'], result, data['article'])
    else:
        text = TXT_ERROR

    await msg.answer(text)
    await state.finish()







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


# @disp.message_handler()
# async def search_message(msg: Message):

    # await msg.answer(text)


def run_bot():
    executor.start_polling(disp)
