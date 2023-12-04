from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, bot



async def create_all_channels_link():
    channels = db.get_channels_data()
    markup = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        link = channel[3]
        markup.insert(InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=link))
    markup.insert(InlineKeyboardButton(text="Tekshirish", callback_data="check_subs"))
    return markup
        


