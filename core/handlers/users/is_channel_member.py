import asyncio
from aiogram import types

from loader import dp, db, bot

from aiogram.dispatcher.filters import Text

from utils.misc.subscription import check


from keyboards.default.for_users import ReplyKeyboardRemove as remove_button

from states.users import UserState



@dp.callback_query_handler(Text(equals="check_subs", ignore_case=True), state="*")
async def check_subs_queryback(query: types.CallbackQuery):

    is_member = await check(query.message.chat.id)

    if is_member:
        text = "✅ Siz barcha kanallarga a'zo bo'lgansiz! Bo‘tdan to‘liq ravishda foydalanishingiz mumkin!."
        await query.answer(text=text, show_alert=True)
        await asyncio.sleep(1)
        await query.message.delete()

        text = "Assalomu alaykum hurmatli abituriyent. Siz Sarbon o'quv markazining rasmiy botidan foydalanayapsiz!"
        await query.message.answer(text=text, reply_markup=remove_button())

        text = "Javoblar varaqasi ID raqamini kiriting."
        await query.message.answer(text=text)

    else:
        alert_text = "Siz barcha kanallarga a'zo bo'lmagansiz! Iltimos a'zo bo'ling!"
        await bot.answer_callback_query(callback_query_id=query.id, text=alert_text, show_alert=True)
 

