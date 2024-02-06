# bot/handlers/start.md 

## Модуль `start.py`

### Обработчик команды `/start`

Модуль `start.py` содержит обработчик команды `/start`, который активируется при вызове пользователем данной команды в чате с ботом.

#### Основной функционал:

1. **Приветственное сообщение**: Бот отправляет пользователю приветственное сообщение с текстом "Привет! Это бот. Я готов к работе!"

```python
from aiogram import types
from database.database import SQLiteDatabaseManager

async def start_command(message: types.Message):
    # Обработчик команды /start
    await message.answer("Привет! Это YLoader. Я готов к работе!")

    # Получение информации о пользователе
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка наличия пользователя в базе данных
    with SQLiteDatabaseManager() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, user_id INTEGER)''')  
        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            # Внесение пользователя в базу данных, если его нет
            cursor.execute('''INSERT INTO users (username, user_id) VALUES (?, ?)''', (username, user_id))

```
