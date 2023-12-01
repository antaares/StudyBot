from aiogram import executor

from loader import dp, db, bot
import middlewares, filters, handlers



async def on_startup(dispatcher):
    db.create_table_users()
    
    


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
