import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from src.bot.keyboards import greet_kb, markup3, search_filter
from src.bot.texts import TXT_HELP, TXT_WELCOME
from src.core.enums import Commands
from src.markets.wildberiies import WbProduct
from src.settings import bot_config

# bot_configure logging
logging.basic(level=logging.INFO)


bot = Bot(
    token=bot_config.bot_token.get_secret_value(),
    parse_mode='HTML'
)
disp = Dispatcher(bot)

@disp.message_handler(commands=['hi3'])
async def process_hi3_command(message: Message):
    await message.reply("Третье - добавляем больше кнопок", reply_markup=markup3)

@disp.message_handler(commands=[Commands.START])
async def start_command(message: Message):
    await message.reply("Прив!", reply_markup=greet_kb)

@disp.message_handler(commands=[Commands.HELP])
async def help_command(msg: Message):
    """This handler will be called when user sends `/start` or `/help` command
    """
    await msg.answer(TXT_HELP.format_map(Commands.as_dict()))

@disp.message_handler(commands=Commands.SEARCH)
async def search_command(msg: Message, command: Command.CommandObj):
    await msg.answer(
        f"Привет, {command.text} \n {command.args}",
        reply_markup=search_filter
    )

@disp.message_handler()
async def echo_message(msg: Message):
    await bot.send_message(msg.from_user.id, msg.text)

def run_bot():
    executor.start_polling(disp)
