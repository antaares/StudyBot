from typing import Union

from aiogram import Bot

from loader import db


async def check(user_id):
    bot = Bot.get_current()
    FinalSatatus = True
    channels = db.get_channels()
    for channel in channels:
        member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
        FinalSatatus *= member.is_chat_member()
    return FinalSatatus