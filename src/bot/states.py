
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()


class UserState(StatesGroup):
    article = State()
    query = State()
    address = State()
