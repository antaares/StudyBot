from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext

from filters.is_private import IsPrivate


from loader import dp, db 


from keyboards.default.for_users import contact_button, ReplyKeyboardRemove as remove_button

from states.users import UserState






@dp.message_handler(IsPrivate(),CommandStart())
async def bot_start_get_contact(message: types.Message):
    await message.answer(
        text="Assalomu alaykum hurmatli abituriyent. Siz Sarbon o'quv markazining rasmiy botidan foydalanayapsiz!",
        reply_markup=types.ReplyKeyboardRemove())
    text = "Hurmatli foydalanuvhchi, <b>Kontaktni ulashish</b> tugmasini bosib telefon raqamingizni yuboring."
    await message.answer(text=text, reply_markup=contact_button)
    await UserState.GetContact.set()
    db.add_user(
        user_id= message.from_user.id
    )


@dp.message_handler(IsPrivate(), content_types=types.ContentType.CONTACT, state=UserState.GetContact)
async def get_contact(message: types.Message, state: FSMContext):
    user = message.from_user
    contact = message.contact
    if contact.user_id and contact.user_id == user.id:
        db.update_user(
            user_id = user.id,
            phone_number = contact.phone_number)
        text = "Hurmatli foydalanuvhchi, siz ro'yxatdan o'tdingiz!\nNatijalaringizni\
          bilish uchun sizga berilgan maxsus id raqamini kiriting."
        await message.answer(text=text, reply_markup= remove_button())
        await state.finish()
    elif not contact.user_id:
        db.update_user(
            user_id= user.id,
            phone_number= contact.phone_number
        )
        text = "Hurmatli foydalanuvhchi, siz ro'yxatdan o'tdingiz!\nNatijalaringizni\
          bilish uchun sizga berilgan maxsus id raqamini kiriting."
        await message.answer(text=text, reply_markup=remove_button)
        await state.finish()
    else:
        text = "Iltimos faqatgina tugmani bosish orqali telefon raqamingizni yuboring!"
        await message.answer(text, contact_button)
        await UserState.GetContact.set()

        



@dp.message_handler(IsPrivate(), commands="error")
async def error(message: types.Message):
    await message.answer_document(document=open("logfile_err.log", "rb"))