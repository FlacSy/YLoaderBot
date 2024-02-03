import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from database.database import SQLiteDatabaseManager
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.is_admin import IsAdmin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import USE_AD

class AdvertiseStates(StatesGroup):
    waiting_for_media = State()
    waiting_for_text = State()

async def cmd_start_advertise(message: Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin:  
        await message.answer("Давайте начнем создание рекламы. Пожалуйста, загрузите медиа контент.")
        await AdvertiseStates.waiting_for_media.set()

async def handle_media_content(message: Message, state: FSMContext):
    media_file = message.photo[-1] if message.photo else message.video
    media_path = f"media/{media_file.file_id}.jpg" 

    await media_file.download(media_path)

    await state.update_data(media_path=media_path)

    await message.answer("Медиа контент успешно загружен. Теперь введите текст для рекламы.")
    await AdvertiseStates.waiting_for_text.set()

async def handle_ad_text(message: Message, state: FSMContext):
    ad_text = message.text

    data = await state.get_data()
    media_path = data.get("media_path")

    with SQLiteDatabaseManager() as db_cursor:
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS ad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_path TEXT,
                ad_text TEXT
            )
        """)

        db_cursor.execute("INSERT INTO ad (media_path, ad_text) VALUES (?, ?)", (media_path, ad_text))


    await state.finish()

    await message.answer(f"Реклама успешно создана:\n{hbold('Текст:')} {ad_text}\n{hbold('Медиа контент:')} {media_path}")

async def cmd_cancel(message: Message, state: FSMContext):
    data = await state.get_data()
    media_path = data.get("media_path")
    if media_path:
        os.remove(media_path)

    await state.finish()
    await message.answer("Вы отменили создание рекламы.")

async def cmd_show_ad_list(message: Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin: 
        with SQLiteDatabaseManager() as db_cursor:
            db_cursor.execute("SELECT ad_text, media_path FROM ad")
            ads = db_cursor.fetchall()

        if not ads:
            await message.answer("Список рекламы пуст.")
            return

        ad_list_text = "Список рекламы:\n"
        for ad in ads:
            ad_list_text += f"{hbold('Текст:')} {ad[0]}\n{hbold('Медиа контент:')} {ad[1]}\n\n"

        await message.answer(ad_list_text)

async def cmd_delete_ad(message: Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin:
        with SQLiteDatabaseManager() as db_cursor:
            db_cursor.execute("SELECT id, ad_text, media_path FROM ad")
            ads = db_cursor.fetchall()

        if not ads:
            await message.answer("Список рекламы пуст.")
            return

        keyboard = InlineKeyboardMarkup()
        for ad in ads:
            ad_id = ad[0]
            ad_text = ad[1]
            media_path = ad[2]
            button_text = f"{ad_text} - {media_path}"
            keyboard.add(InlineKeyboardButton(button_text, callback_data=f"delete_ad_{ad_id}"))

        await message.answer("Выберите рекламу для удаления:", reply_markup=keyboard)

async def delete_ad(callback_query: types.CallbackQuery):
    ad_id = int(callback_query.data.split('_')[-1])

    with SQLiteDatabaseManager() as db_cursor:
        db_cursor.execute("SELECT ad_text, media_path FROM ad WHERE id=?", (ad_id,))
        ad = db_cursor.fetchone()

        if ad:
            ad_text = ad[0]
            media_path = ad[1]

            db_cursor.execute("DELETE FROM ad WHERE id=?", (ad_id,))
            os.remove(media_path)

            await callback_query.answer("Реклама успешно удалена.")
        else:
            await callback_query.answer("Не удалось найти рекламу.")

async def cmd_ad_state(message: Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()
    
    if is_admin: 
        if USE_AD:
            await message.answer("Реклама включена")
        else:
            await message.answer("Реклама выключена")