# Обработчики команды /start
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from database.database import SQLiteDatabaseManager

async def start_command(message: types.Message):
    # Обработчик команды /start
    await message.answer("Привет! Это YLoader. Я готов к работе!")

    # Получение информации о пользователе
    user_id = message.from_user.id
    username = message.from_user.username

    # Внесение пользователя в базу данных
    with SQLiteDatabaseManager() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, user_id INTEGER)''')  
        cursor.execute('''INSERT INTO users (username, user_id) VALUES (?, ?)''', (username, user_id))

# Регистрация обработчика команды /start
__all__ = ['start_command']
