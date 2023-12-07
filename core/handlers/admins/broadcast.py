import asyncio
from states.admins import AdminState
from utils.db_api.database import Database
from handlers.admins.keyboards import BACK, CHOICE, CONFIRM, login_page_keyboard
from loader import dp, db, bot

from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate







# send message to all users
@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='📨 Xabar yuborish'), state="*")
async def broadcast(message: types.Message, state: FSMContext):
    text = "Ho‘sh, demak boshladik, menga barcha foydalanuvchilarga yubormoqchi bo‘lgan xabaringizni yuboring:"
    await message.answer(text=text, reply_markup=BACK)
    await AdminState.getMessage.set()






@dp.message_handler(IsPrivate(), content_types=types.ContentType.ANY, state=AdminState.getMessage)
async def get_message(message: types.Message, state: FSMContext):
    text = message.text

    if text == "Bekor qilish":
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=login_page_keyboard)
        await state.finish()
        return
    
    MessageID = message.message_id
    ChatID = message.chat.id
    await state.update_data(MessageID=MessageID)
    await state.update_data(ChatID=ChatID)

    await message.answer(text="Qaysi usulda yuboramiz?", reply_markup=CHOICE)
    await AdminState.Choice.set()


    






@dp.message_handler(IsPrivate(), state=AdminState.Choice)
async def choiceMethod(message: types.Message, state: FSMContext):
    text = message.text

    if text == "Bekor qilish":
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=login_page_keyboard)
        await state.finish()
        return
    
    Method = message.text
    await state.update_data(Method=Method)

    data = await state.get_data()
    MessageID = data['MessageID']
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Shu xabarni yuboramizmi?",
        reply_to_message_id=MessageID,
        reply_markup=CONFIRM
    )
    await AdminState.Confirm.set()




@dp.message_handler(IsPrivate(), state=AdminState.Confirm)
async def Sending(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Yuborish":
        data = await state.get_data()
        Method = data['Method']
        ChatID = data['ChatID']
        if Method == "Forward Message":
            count, inactives = await SEND_FORWARD(db, bot, state)
            send_text = f"Tayyor, sizning xabaringiz {count} ta foydalanuvchiga yetkazildi...\n"
            send_text += f"{len(inactives)} ta foydalanuvchiga xabar yetkazilmadi..."
            await dp.bot.send_message(chat_id=ChatID, text=send_text, reply_markup=login_page_keyboard)
        else:
            count, inactives = await SEND_COPY(db, bot, state)
            send_text = f"Tayyor, sizning xabaringiz {count} ta foydalanuvchiga yetkazildi...\n"
            send_text += f"{len(inactives)} ta foydalanuvchiga xabar yetkazilmadi..."
            await dp.bot.send_message(chat_id=ChatID, text=send_text, reply_markup=login_page_keyboard)
    else:
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=login_page_keyboard)
        await state.finish()
        return
    await state.finish()
    db.restatus_users(inactives)








async def SEND_COPY(db: Database, bot: Bot, state: FSMContext):
    users = db.all()
    data = await state.get_data()
    ChatID = data['ChatID']
    MessageID = data['MessageID']
    count = 0

    inactives = []

    for user in users:
        try:
            await bot.copy_message(chat_id=user, from_chat_id=ChatID, message_id=MessageID)
            count += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(e)
            inactives.append(user)
    return count, inactives


async def SEND_FORWARD(db: Database, bot: Bot, state: FSMContext):
    users = db.all()
    data = await state.get_data()
    ChatID = data['ChatID']
    MessageID = data['MessageID']
    count = 0

    inactives = []

    for user in users:
        try:
            await bot.forward_message(chat_id=user, from_chat_id=ChatID, message_id=MessageID)
            count += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(e)
            inactives.append(user)
    return count, inactives