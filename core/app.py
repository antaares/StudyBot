from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers



async def on_startup(dispatcher):
    db.create_table_users()
    db.create_table_admins()
    db.create_table_channels()
    
    


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
