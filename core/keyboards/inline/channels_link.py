from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot



async def create_all_channels_link():
    channels = db.get_channels()
    markup = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        link = await bot.export_chat_invite_link(chat_id=channel)
        markup.insert(InlineKeyboardButton(text=channel.title[:30], url=link))
    markup.insert(InlineKeyboardButton(text="Tekshirish", callback_data="check_subs"))
    return markup
        


