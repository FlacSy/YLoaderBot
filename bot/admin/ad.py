import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from database.database import SQLiteDatabaseManager
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.is_admin import IsAdmin

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
