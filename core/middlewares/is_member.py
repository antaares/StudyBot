import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

# from data.config import CHANNELS
from utils.misc import subscription
from loader import bot

from keyboards.inline.channels_link import create_all_channels_link


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):        
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.message.contact:
            print("contact")
            return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
            
        

        else:
            return

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        markup = await create_all_channels_link()
        final_status = await subscription.check(user)


        if not final_status:
            await update.message.answer(result, reply_markup=markup,disable_web_page_preview=True)
            raise CancelHandler()