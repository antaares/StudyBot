import asyncio
from states.admins import AdminState
from utils.db_api.database import Database
from handlers.admins.keyboards import BACK, YES_NO, manage_admins_keyboard, login_page_keyboard
from loader import dp, db, bot

from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate





@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='👥 Adminlar'), state="*")
async def manage_admins(message: types.Message, state: FSMContext):
    admins = db.get_admins()
    await message.answer(
        text=f"Adminlarni boshqarish\n"\
            "Adminlar soni: {len(admins)}", 
        reply_markup=manage_admins_keyboard)



@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Admin qo'shish"))
async def add_admin(message: types.Message, state: FSMContext):
    await message.answer(
        text="Yangi admin foydalanuvchini ID raqamini kiriting,\n \
            Botga /info buyrug'ini yuboring va foydalanuvchi ID raqamini bilib oling", 
        reply_markup=BACK)
    await AdminState.AdminID.set()


@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.AdminID)
async def get_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    if admin_id.isdigit():
        admin_id = int(admin_id)
        if db.is_admin(admin_id):
            await message.answer(
                text="Bu foydalanuvchi allaqachon adminlar ro'yxatida mavjud",
                reply_markup = manage_admins_keyboard)
            await state.finish()
        else:
            await state.update_data(admin_id=admin_id)
            await message.answer(
                text="Admin ismini kiriting", 
                reply_markup=BACK)
            await AdminState.AdminName.set()
    else:
        await message.answer(
            text="Foydalanuvchi ID raqamini kiriting, faqat raqamlardan foydalaning", 
            reply_markup=BACK)
        await AdminState.AdminID.set()


@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.AdminName)
async def get_admin_name(message: types.Message, state: FSMContext):
    admin_name = message.text
    await state.update_data(admin_name=admin_name)
    await message.answer(
        text="Yangi adminni qo'shishni tasdiqlaysizmi?", 
        reply_markup=YES_NO)
    await AdminState.ConfirmAdmin.set()


@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.ConfirmAdmin)
async def confirm_add_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_id = data.get("admin_id")
    admin_name = data.get("admin_name")
    if message.text == "Ha":
        db.add_admin(admin_id, admin_name)
        await message.answer(
            text="Yangi admin qo'shildi", 
            reply_markup=manage_admins_keyboard)
        await state.finish()
    elif message.text == "Yo'q":
        await message.answer(
            text="Yangi admin qo'shilmadi", 
            reply_markup=manage_admins_keyboard)
        await state.finish()
    else:
        await message.answer(
            text="Iltimos, tugmalardan birini bosing", 
            reply_markup=YES_NO)
        await AdminState.ConfirmAdmin.set()



@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Admin o'chirish"))
async def delete_admin(message: types.Message, state: FSMContext):
    await message.answer(
        text="O'chirmoqchi bo'lgan adminning id raqamini yuboring:", 
        reply_markup=BACK
        )
    await AdminState.DelAdminID.set()



@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.DelAdminID)
async def get_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    if admin_id.isdigit():
        admin_id = int(admin_id)
        if db.is_admin(admin_id):
            await state.update_data(admin_id=admin_id)
            await message.answer(
                text="Adminni o'chirishni tasdiqlaysizmi?", 
                reply_markup=YES_NO)
            await AdminState.DelConfirm.set()
        else:
            await message.answer(
                text="Bunday admin mavjud emas", 
                reply_markup=manage_admins_keyboard)
            await state.finish()
    else:
        await message.answer(
            text="Foydalanuvchi ID raqamini kiriting, faqat raqamlardan foydalaning", 
            reply_markup=BACK)
        await AdminState.DelAdminID.set()




@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.DelConfirm)
async def confirm_delete_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_id = data.get("admin_id")
    if message.text == "Ha":
        db.delete_admin(admin_id)
        await message.answer(
            text="Admin o'chirildi", 
            reply_markup=manage_admins_keyboard)
        await state.finish()
    elif message.text == "Yo'q":
        await message.answer(
            text="Admin o'chirilmadi", 
            reply_markup=manage_admins_keyboard)
        await state.finish()
    else:
        await message.answer(
            text="Iltimos, tugmalardan birini bosing", 
            reply_markup=YES_NO)
        await AdminState.DelConfirm.set()


@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Adminlar ro'yxati"), state="*")
async def get_admins(message: types.Message, state: FSMContext):
    admins = db.get_admins()
    if len(admins) == 0:
        await message.answer(
            text="Hozircha adminlar ro'yxatida hech kim yo'q", 
            reply_markup=manage_admins_keyboard)
        await state.finish()
    else:
        text = "Adminlar ro'yxati:\n"
        for admin in admins:
            text += f"Admin id: <code>{admin[0]}</code> - Ismi: {admin[1]}\n"
        await message.answer(
            text=text, 
            reply_markup=manage_admins_keyboard)
        await state.finish()


@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Bosh menu"), state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer(
        text="Qanday amal bajaramiz?", 
        reply_markup=login_page_keyboard)
    await state.finish()


