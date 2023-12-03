from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    GetID = State()
    GetContact = State()