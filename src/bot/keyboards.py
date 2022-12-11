from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.core.enums import Commands

btn_search = KeyboardButton(Commands.SEARCH)
btn_cancel = KeyboardButton(Commands.CANCEL)

main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder='Начать поиск',
    keyboard=[
        [btn_search, btn_cancel]
    ]
)

cancel_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [btn_cancel]
    ]
)
