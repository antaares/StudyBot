from aiogram import Dispatcher
from filters.is_admin import IsAdmin, IsChatAdmin
from filters.is_group import IsGroup
from filters.is_private import IsPrivate

from loader import dp
# from .is_admin import AdminFilter


if __name__ == "filters":
    #dp.filters_factory.bind(is_admin)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsChatAdmin)
    pass
