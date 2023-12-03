import os
from aiogram import types

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import force_reply

from filters.is_private import IsPrivate
from states.users import UserState

from loader import dp, db



@dp.message_handler(IsPrivate(), state=None, content_types=types.ContentTypes.TEXT)
async def getId(message: types.Message, state: FSMContext):
    id = message.text
    path = f"./core/files/unzips/{id}.pdf"
    if os.path.isfile(path):
        await message.answer_chat_action(action="upload_document")
        with open(path, 'rb') as file:
            await message.answer_document(document=file, caption=f"{id} id raqamli natijalar fayli.")
            await message.answer("Javoblar varaqasi ID raqamini kiriting.")
            await state.finish()
            return
    await message.answer("Siz yuborgan id ga mos fayl topilmadi. ID raqam to‘g‘ri ekanligini tekshirib ko'ring!")
    await state.finish()
