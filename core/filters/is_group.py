#  import BoundFilter from aiogram.dispatcher.filters
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import dp, db




class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (types.ChatType.SUPERGROUP, types.ChatType.GROUP)
    
