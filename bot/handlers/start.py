from aiogram import types
from database.database import SQLiteDatabaseManager
from typing import Optional

async def start_command(message: types.Message) -> None:
    # Обработчик команды /start
    await message.answer("Привет! Это YLoader. Я готов к работе!")

    # Получение информации о пользователе
    user_id: int = message.from_user.id
    username: Optional[str] = message.from_user.username

    # Проверка наличия пользователя в базе данных
    with SQLiteDatabaseManager() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, user_id INTEGER)''')  
        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
        existing_user: Optional[tuple] = cursor.fetchone()

        if not existing_user:
            # Внесение пользователя в базу данных, если его нет
            cursor.execute('''INSERT INTO users (username, user_id) VALUES (?, ?)''', (username, user_id))
