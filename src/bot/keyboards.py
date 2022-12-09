from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.core.enums import CallBackData

start_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(
    'Конечно!', callback_data=CallBackData.OFFCOURSE)
)
