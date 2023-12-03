from aiogram import types

from loader import dp, db

from aiogram.dispatcher.filters import Text

from utils.misc.subscription import check


from keyboards.default.for_users import contact_button

from states.users import UserState



@dp.callback_query_handler(Text(equals="check_subs"))
async def check_subs_queryback(query: types.CallbackQuery):
    await query.answer(cache_time=60)
    is_member = await check(query.message.chat.id)
    if is_member:
        text = "Siz kanallarga a'zo bo'lgansiz!"
        await query.answer(text=text, show_alert=True)
        await query.message.delete()

        text = "Hurmatli foydalanuvhchi, <b>Kontaktni ulashish</b> tugmasini bosib telefon raqamingizni yuboring."
        await query.message.answer(text=text, reply_markup=contact_button)
        await UserState.GetContact.set()
        return
    
    alert_text = "Siz barcha kanallarga a'zo bo'lmagansiz!"
    await query.answer(
        text= alert_text,
        show_alert= True
    )

