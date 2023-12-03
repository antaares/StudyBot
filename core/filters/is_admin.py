#  import BoundFilter from aiogram.dispatcher.filters
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


from data.config import ADMINS
from loader import db



class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        admins = db.get_admins()
        return message.from_user.id in ADMINS or message.from_user.id in [admin[0] for admin in admins]


class IsChatAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()