from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove




contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kontaktni ulashish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)