from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate

from loader import dp, db, bot

from handlers.admins.keyboards import get_data_excel_keyboard, login_page_keyboard






@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='📊 Statistika'), state="*")
async def statistika(message: types.Message, state: FSMContext):
    users = db.all()
    inactiv_users = db.inactive_users()
    await message.answer(f"Botning jami foydalanuvchilari: {len(users)}.\n"\
                         f"Botni bloklagan foydalanuvchilar soni {len(inactiv_users)}", 
                         reply_markup=get_data_excel_keyboard)


import sqlite3
import pandas as pd
from io import BytesIO

def extract_to_excel():
    conn = sqlite3.connect('./core/data/main.db')
    data = pd.read_sql_query("SELECT * FROM users", conn)

    # Close the database connection
    conn.close()

    # Export the data to an Excel file
    excel_file_name = './core/data/data.xlsx'
    data.to_excel(excel_file_name, index=False)
    return excel_file_name




# extract_to_excel()



def get_data_from_db():
    conn = sqlite3.connect('./core/data/main.db')
    data = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return data

# Function to create Excel file in memory and return BytesIO object
def create_excel_buffer(data):
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_buffer.seek(0)
    return excel_buffer





@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='📥 Excel fayl yuklash'), state="*")
async def get_data_excel(message: types.Message, state: FSMContext):
    data = get_data_from_db()
    excel_buffer = create_excel_buffer(data)
    await bot.send_document(
        message.from_user.id, 
        types.InputFile(excel_buffer, filename="Foydalanuvchilar.xlsx"), 
        caption='Foydalanuvchilar ro`yxati'
        )



@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='Bosh menu'), state="*")
async def bosh_menu(message: types.Message, state: FSMContext):
    await message.answer(text="Qanday amal bajaramiz?", reply_markup=login_page_keyboard)
    await state.finish()
