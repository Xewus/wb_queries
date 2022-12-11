from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.keyboards import cancel_kb, main_kb
from src.bot.states import UserState, storage
from src.bot import texts
from src.core.enums import Commands
from src.core.utils import get_geo_coord
from src.markets.wildberiies import WbProduct
from src.settings import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    parse_mode='HTML'
)

disp = Dispatcher(bot, storage=storage)


@disp.message_handler(commands=[Commands.START])
async def cmd_start(msg: Message):
    await msg.answer(texts.START)
    await msg.answer(texts.DESCRIPTION, reply_markup=main_kb)


@disp.message_handler(
    Text(equals=Commands.CANCEL.value),
    state=UserState.all_states
)
async def cmd_cansel(msg: Message, state: FSMContext):
    await state.finish()
    await msg.reply(texts.CANCEL, reply_markup=main_kb)


@disp.message_handler(Text(equals=Commands.SEARCH.value))
async def cmd_search(msg: Message):
    await msg.answer(texts.INPUT_ARTICLE, reply_markup=ReplyKeyboardRemove())
    await UserState.article.set()


@disp.message_handler(state=UserState.article)
async def get_article(msg: Message, state: FSMContext):
    if not msg.text.isdecimal():
        await msg.answer(texts.ERROR_QUERY, reply_markup=cancel_kb)
        return await msg.answer(texts.INPUT_ARTICLE)

    article = int(msg.text)
    name = await WbProduct(article).get_product_name()

    if name is None:
        state.finish()
        return await msg.answer(
            texts.ANSWER_NOT_FOUND % ('', 0, msg.text),
            reply_markup=main_kb
        )

    await state.update_data(article=article)
    await msg.reply(name, reply_markup=cancel_kb)
    await msg.answer(texts.INPUT_QUERY)
    await UserState.next()


@disp.message_handler(state=UserState.query)
async def get_query(msg: Message, state: FSMContext):
    await state.update_data(query=msg.text)
    await msg.answer(texts.INPUT_ADDRESS, reply_markup=cancel_kb)
    await UserState.address.set()


@disp.message_handler(state=UserState.address)
async def get_addres(msg: Message, state: FSMContext):
    address, *_ = await get_geo_coord(msg.text)
    await msg.answer(address)
    await state.update_data(address=msg.text)
    data = await state.get_data()

    await msg.answer(
        texts.ALL_DATA % (data["article"], data["query"], address)
    )

    result = await WbProduct(
        data['article']
    ).get_place_on_page(
        query=data['query'],
        address=data['address']
    )

    if isinstance(result, dict):
        text = texts.ANSWER_WITH_DATA.format_map(result)
    elif isinstance(result, int):
        text = texts.ANSWER_NOT_FOUND % (
            data['query'], result, data['article']
        )
    else:
        text = texts.ERROR

    await msg.answer(text, reply_markup=main_kb)
    await state.finish()


@disp.message_handler()
async def some_message(msg: Message):
    await msg.answer(texts.DEFAULT)
    await msg.answer(texts.DESCRIPTION, reply_markup=main_kb)


def run_bot():
    executor.start_polling(disp)
