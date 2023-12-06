import asyncio
from states.admins import AdminState
from utils.db_api.database import Database
from handlers.admins.keyboards import YES_NO, login_page_keyboard, manage_channels_keyboard, BACK
from loader import dp, db, bot

from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate



# manage channels
@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="🎞 Kanallar"))
async def manage_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(
        text=f"Kanallarni boshqarish\n"\
            "Kanallar soni: {len(channels)}", 
        reply_markup=manage_channels_keyboard)



@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Kanal qo'shish"))
async def add_channel(message: types.Message, state: FSMContext):
    await message.answer(
        text="<b>ESLATMA:</b> Kanalni qo'shish uchun kanalga botni admin qiling.",
        parse_mode="HTML"
        )
    await message.answer(
        text="Majburiy a'zolik uchun yangi kanal qo'shish uchun shu kanalga joylangan istalgan xabarni botga yuboring", 
        reply_markup=BACK)
    await AdminState.ForwardingMessage.set()




@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.ForwardingMessage, content_types=types.ContentType.ANY)
async def get_forwarding_message(message: types.Message, state: FSMContext):
    if message.forward_from_chat is not None and message.forward_from_chat.type == "channel":
        ChannelID = message.forward_from_chat.id
        ChannelNAME = message.forward_from_chat.title
        if db.in_channel(ChannelID):
            await message.answer(
                text="Bu kanal allaqachon ro'yxatda mavjud",
                reply_markup = manage_channels_keyboard)
            await state.finish()
        else:
            await state.update_data(channel_id=ChannelID, channel_name=ChannelNAME)
            # check bot is admin in channel
            try:
                bot_id = (await bot.get_me()).id
                chat_member = await bot.get_chat_member(chat_id=ChannelID, user_id=bot_id)
                if chat_member.is_chat_admin():
                    invite_link = await bot.create_chat_invite_link(chat_id=ChannelID)
                    await state.update_data(invite_link=invite_link.invite_link)
                    print(f"invite link: {invite_link.invite_link}")
                    await message.answer(
                        text="Kanal botga muvafaqqiyatli ulandi.",
                        reply_markup=manage_channels_keyboard)
                    
                    db.add_channel(ChannelID, ChannelNAME, invite_link.invite_link) 
                        
                else:
                    await message.answer(
                        text="Bot kanalga admin emas, botni kanalga admin qiling 1", 
                        reply_markup=BACK)
                await state.finish()
               
            except Exception as e:
                print(f"THE ERROR: {e}")
                await message.answer(
                    text="Bot kanalga admin emas, botni kanalga admin qiling 2", 
                    reply_markup=BACK)
                await state.finish()
    else:
        await message.answer(
            text="Faqat kanallarni qo'shishingiz mumkin. Iltimos, \
                kanalga botni admin qiling va botga kanaldan istalgan xabarni yuboring",
            reply_markup=BACK)
        await AdminState.ForwardingMessage.set()






@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Kanal o'chirish"))
async def delete_channel(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    if len(channels) == 0:
        await message.answer(
            text="Kanal ro'yxati bo'sh", 
            reply_markup=manage_channels_keyboard)
    else:
        await message.answer(
            text="O'chirish uchun kanal id raqamini yozing:", 
            reply_markup=BACK)
        await AdminState.ChannelID.set()



@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.ChannelID)
async def get_channel_id(message: types.Message, state: FSMContext):
    channel_id = message.text.replace("-", "")
    if channel_id.isdigit():
        channel_id = int(channel_id) * -1
        if db.in_channel(channel_id):
            await state.update_data(channel_id=channel_id)
            await message.answer(
                text="Kanalni o'chirishni tasdiqlaysizmi?", 
                reply_markup=YES_NO)
            await AdminState.ChannelDeleteConfirm.set()
        else:
            await message.answer(
                text="Bunday kanal mavjud emas", 
                reply_markup=manage_channels_keyboard)
            await state.finish()
    else:
        await message.answer(
            text="Iltimos, kanal id raqamini yozing", 
            reply_markup=BACK)
        await AdminState.ChannelID.set()




@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.ChannelDeleteConfirm)
async def confirm_delete_channel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get("channel_id")
    if message.text == "Ha":
        db.delete_channel(channel_id)
        await message.answer(
            text="Kanal o'chirildi", 
            reply_markup=manage_channels_keyboard)
        await state.finish()
    elif message.text == "Yo'q":
        await message.answer(
            text="Kanal o'chirilmadi", 
            reply_markup=manage_channels_keyboard)
        await state.finish()
    else:
        await message.answer(
            text="Iltimos, tugmalardan birini bosing", 
            reply_markup=YES_NO)
        await AdminState.ChannelDeleteConfirm.set()






# list of existing channels
@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Kanallar ro'yxati"))
async def list_of_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels_data()
    if len(channels) == 0:
        await message.answer(
            text="Kanal ro'yxati bo'sh.", 
            reply_markup=manage_channels_keyboard)
    else:
        text = "Kanallar ro'yxati:\n\n"
        for channel in channels:
            text += f"📢 <b><a href=\"{channel[3]}\">{channel[2][:20]}</a></b> -  ChannelID: <code>{channel[1]}</code>\n"
        await message.answer(
            text=text, 
            reply_markup=manage_channels_keyboard,
            parse_mode="HTML")