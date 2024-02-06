# bot/main.py

## Модуль `main.py`

Модуль `main.py` содержит основной код бота, включая инициализацию, регистрацию хендлеров, и запуск бота.

#### Основной функционал:

1. **Инициализация бота и диспетчера**: Создание объектов `Bot` и `Dispatcher`, инициализация памяти.

2. **Регистрация хендлеров**: Регистрация всех необходимых хендлеров для команд, состояний и callback query.

3. **Запуск бота**: Запуск бота с использованием `executor.start_polling`.

4. **Проверка наличия администратора**: При запуске производится проверка наличия администратора. Если администратор отсутствует, запрашивается ввод ID пользователя для добавления в администраторы.

#### Код модуля:

```python
import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage  
from config.secrets import BOT_TOKEN
from config.settings import USE_AD
from bot.handlers import start, help, url
from bot.admin import log, ad
from utils import helpers, add_admin
from utils.ad_timer import send_advertisements
from database.database import SQLiteDatabaseManager

# Initialize MemoryStorage
storage = MemoryStorage()

# Initialize bot and dispatcher with MemoryStorage
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Logging start of the bot
logging.info('Bot has been started')

# Function to register handlers
async def register_handlers():
    # Check for the presence of an administrator
    admin_id = get_admin_id()
    if admin_id is None:
        print("Admin ID is not set. Please enter a user ID to add to administrators.")
        try:
            user_id = int(input("Enter the user ID to add to administrators: "))
            add_admin.add_admin(user_id)
        except ValueError:
            print("Incorrect input of user ID. Please enter an integer.")
            return
        
    # Command handlers
    dp.register_message_handler(start.start_command, commands=['start', 'about'])
    dp.register_message_handler(help.help_command, commands=['help', 'info'])
    dp.register_message_handler(log.log_command, commands=['log'])
    dp.register_message_handler(ad.cmd_start_advertise, commands=['ad_start'])
    dp.register_message_handler(ad.cmd_cancel, commands=["cancel_ad"], state="*")
    dp.register_message_handler(ad.cmd_show_ad_list, commands="show_ad_list", state="*")
    dp.register_message_handler(ad.cmd_delete_ad, commands="delete_ad", state="*")
    dp.register_message_handler(ad.cmd_ad_state, commands="ad_state", state="*")
    # FSM handlers
    dp.register_message_handler(ad.handle_media_content, content_types=types.ContentType.PHOTO, state=ad.AdvertiseStates.waiting_for_media) 
    dp.register_message_handler(ad.handle_ad_text, content_types=types.ContentType.TEXT, state=ad.AdvertiseStates.waiting_for_text)
    dp.register_message_handler(url.url_handler, lambda message: not re.match(r'format_', message.text.lower()))
    dp.register_message_handler(url.url_handler, content_types=types.ContentType.TEXT)
    # Callback query handlers
    dp.register_callback_query_handler(url.handle_format_choice, lambda callback_query: callback_query.data.lower().startswith('format_'))

def get_admin_id():
    try:
        with SQLiteDatabaseManager() as db:
            db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
            result = db.execute("SELECT user_id FROM admins LIMIT 1").fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error in get_admin_id: {e}")
        return None

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register_handlers())
    executor.start_polling(dp, on_startup=helpers.on_startup, on_shutdown=helpers.on_shutdown, skip_updates=True)
    
    if USE_AD:
        loop.run_until_complete(send_advertisements(bot=bot))
```