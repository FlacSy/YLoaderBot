# utils/advertisement_sender.py

## Модуль `advertisement_sender.py`

Модуль `advertisement_sender.py` содержит функции для отправки рекламных материалов пользователям бота в определенный интервал времени.

#### Основной функционал:

1. **Отправка рекламы**: Функция `send_advertisement` отправляет рекламу конкретному пользователю с указанным медиа-контентом и текстом.

2. **Отправка рекламы всем пользователям**: Функция `send_advertisements` периодически проверяет базу данных на наличие пользователей и рекламных материалов, а затем отправляет рекламу каждому пользователю в базе данных.

#### Код модуля:

```python
import asyncio
import logging
from aiogram import Bot
from aiogram.utils import exceptions
from aiogram.types import InputFile, InputMediaPhoto
from database.database import SQLiteDatabaseManager
from config.settings import SEND_INTERVAL_MIN

async def send_advertisement(user_id, media_path, ad_text, bot: Bot):
    # Отправка рекламы конкретному пользователю
    try:
        with open(f'{media_path}', 'rb') as photo:
            media = [InputMediaPhoto(media=InputFile(photo), caption=ad_text)]
            await bot.send_media_group(chat_id=user_id, media=media)
        logging.info(f"Advertisement sent to user {user_id}")
    except exceptions.BotBlocked:
        logging.warning(f"Target user {user_id} blocked the bot")
    except exceptions.ChatNotFound:
        logging.warning(f"Target user {user_id} not found")
    except exceptions.UserDeactivated:
        logging.warning(f"Target user {user_id} is deactivated")
    except exceptions.RetryAfter as e:
        logging.error(f"Sending to user {user_id} is blocked for {e.timeout} seconds. Retry after {e.retry_time} seconds.")
        await asyncio.sleep(e.retry_time)
        await send_advertisement(user_id, media_path, ad_text, bot)
    except exceptions.TelegramAPIError:
        logging.error(f"Error sending advertisement to user {user_id}")

async def send_advertisements(bot):
    # Периодическая отправка рекламы всем пользователям
    while True:
        with SQLiteDatabaseManager() as cursor:
            cursor.execute("SELECT user_id FROM users")
            users = cursor.fetchall()

            for user_tuple in users:
                user_id = user_tuple[0]

                cursor.execute("SELECT media_path, ad_text FROM ad")
                ad_info = cursor.fetchone()

                if ad_info:
                    media_path, ad_text = ad_info
                    await send_advertisement(user_id, media_path, ad_text, bot)
        await asyncio.sleep(SEND_INTERVAL_MIN)
```