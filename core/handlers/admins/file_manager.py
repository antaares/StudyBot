import aiohttp
import asyncio
import re




from states.admins import AdminState
from utils.db_api.database import Database
from handlers.admins.keyboards import YES_NO, login_page_keyboard, manage_channels_keyboard, BACK
from loader import dp, db, bot

from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate

from data.config import API_KEY as api_key



# Replace '/path/to/output/directory' with the desired directory to save the downloaded file
output_directory = './core/files/zips'


extract_directory = './core/files/unzips'


# download functions


def extract_file_id_from_url(url):
    # Regular expression pattern to extract the file ID
    pattern = r"/file/d/([a-zA-Z0-9_-]+)"

    # Find matches using the pattern
    match = re.search(pattern, url)

    if match:
        file_id = match.group(1)
        return file_id
    else:
        return None




async def get_file_metadata(file_id, api_key):
    metadata_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name&key={api_key}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(metadata_url) as response:
                if response.status == 200:
                    metadata = await response.json()
                    return metadata.get('name')
                else:
                    print(f"Failed to fetch metadata. Status code: {response.status}")
                    return None

    except Exception as e:
        print(f"An error occurred while fetching metadata: {e}")
        return None



import os

def delete_files_in_folder(file_name):
    try:
        zip_path = os.path.join(output_directory, file_name)
        if os.path.isfile(zip_path):
            os.remove(zip_path)


        files = os.listdir(extract_directory)
        for file_name in files:
            file_path = os.path.join(extract_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)  # or os.unlink(file_path)
                print(f"Deleted: {file_name}")
    except Exception as e:
        print(f"Error deleting files: {e}")






async def download_file_with_api_key(file_id, api_key):
    file_name = await get_file_metadata(file_id, api_key)
    if file_name:
        delete_files_in_folder(file_name)
        download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={api_key}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        output_file_path = f"{output_directory}/{file_name}"
                        with open(output_file_path, 'wb') as output_file:
                            output_file.write(content)
                        return file_name

                    else:
                        return None

        except Exception as e:
            print(f"An error occurred while downloading file: {e}")
            return None









# general menu
# # # # # # #


@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals='📁 Fayl yuklash'), state="*")
async def file_manager(message: types.Message, state: FSMContext):
    text = "Fayl yuklash uchun Google Drive linkini yuboring\n"\
    "ESLATMA: Yangi fayl yuklash davomida serverdagi fayllar o‘chirib yuboriladi."
    await message.answer(
        text=text,
        reply_markup=BACK)
    await AdminState.GetFile.set()


@dp.message_handler(IsPrivate(), IsAdmin(), Text(equals="Bekor qilish"), state="*")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(
        text="Qanday amal bajaramiz!", 
        reply_markup=login_page_keyboard)
    await state.finish()


@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.GetFile)
async def get_file(message: types.Message, state: FSMContext):
    file_link = message.text
    file_id = extract_file_id_from_url(file_link)
    if file_id:
        await state.update_data(file_id=file_id, file_link=file_link)
        await message.answer(
            text="Fayl yuklashni tasdiqlaysizmi?", 
            reply_markup=YES_NO)
        await AdminState.FileConfirm.set()
    else:
        await message.answer(
            text="Google Drive linkini yuboring", 
            reply_markup=BACK)
        await AdminState.GetFile.set()





@dp.message_handler(IsPrivate(), IsAdmin(), state=AdminState.FileConfirm)
async def confirm_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = data.get("file_id")
    if message.text == "Ha":
        await message.answer(
            text="Fayl yuklanmoqda, kuting...", 
            reply_markup=BACK)
        
        file = await download_file_with_api_key(
            file_id = file_id,
            api_key=api_key)
        
        if file is None:
            await message.answer(
                text="Fayl yuklanmadi. Linkni tekshirib qaytadan urining yoki dasturchiga murojaat qiling", 
                reply_markup=login_page_keyboard)
            await state.finish()
            return
        
        await message.answer(
            text="Fayl yuklandi", 
            reply_markup=login_page_keyboard)
        
        extract_zip(file_name=file)

        await state.finish()

    elif message.text == "Yo'q":
        await message.answer(
            text="Fayl yuklanmadi", 
            reply_markup=login_page_keyboard)
        await state.finish()

    else:
        await message.answer(
            text="Iltimos, tugmalardan birini bosing", 
            reply_markup=YES_NO)
        await AdminState.FileConfirm.set()






# extract zip file
#
def extract_zip(file_name):
    import zipfile
    with zipfile.ZipFile(os.path.join(output_directory ,file_name), 'r') as zip_ref:
        zip_ref.extractall(extract_directory)


