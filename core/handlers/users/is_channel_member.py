from aiogram import types

from loader import dp, db, bot

from aiogram.dispatcher.filters import Text

from utils.misc.subscription import check


from keyboards.default.for_users import contact_button, ReplyKeyboardRemove as remove_button

from states.users import UserState



@dp.callback_query_handler(Text(equals="check_subs", ignore_case=True), state="*")
async def check_subs_queryback(query: types.CallbackQuery):

    is_member = await check(query.message.chat.id)

    if is_member:
        text = "Siz kanallarga a'zo bo'lgansiz!"
        await query.answer(text=text, show_alert=True)
        await query.message.delete()

        text = "Hurmatli foydalanuvchi, siz ro'yxatdan o'tdingiz!\nNatijalaringizni "\
        "bilish uchun sizga berilgan maxsus id raqamini kiriting."
        await query.message.answer(text=text, reply_markup=remove_button())
    else:
        alert_text = "Siz barcha kanallarga a'zo bo'lmagansiz!"
        await bot.answer_callback_query(callback_query_id=query.id, text=alert_text, show_alert=True)
 

