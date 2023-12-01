from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.is_private import IsPrivate


from loader import dp, db 


@dp.message_handler(IsPrivate(),CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")
    db.add_user(message.from_user.id, message.from_user.full_name)



@dp.message_handler(IsPrivate(), commands="error")
async def error(message: types.Message):
    await message.answer_document(document=open("logfile_err.log", "rb"))