import os
from aiogram import types

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import force_reply

from filters.is_private import IsPrivate
from states.users import UserState

from loader import dp, db



@dp.message_handler(IsPrivate(), state="*", content_types=types.ContentTypes.TEXT)
async def getId(message: types.Message, state: FSMContext):
    id = message.text
    path = f"./core/files/unzips/{id}.pdf"
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            await message.answer_document(document=file, caption=f"{id} id raqamli fayl")
            text = "Bu bot ===== oquv markazining boti!!!\n\n"
            await message.answer(
                text=text
                )
            await state.finish()
            return
    await message.answer("Siz yuborgan id ga mos fayl topilmadi...")
    await state.finish()
