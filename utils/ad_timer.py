import asyncio
import logging
from aiogram import Bot
from aiogram.utils import exceptions
from aiogram.types import InputFile, InputMediaPhoto
from database.database import SQLiteDatabaseManager
from config.settings import SEND_INTERVAL_MIN
from typing import List, Tuple

async def send_advertisement(user_id: int, media_path: str, ad_text: str, bot: Bot) -> None:
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

async def send_advertisements(bot: Bot) -> None:
    while True:
        with SQLiteDatabaseManager() as cursor:
            cursor.execute("SELECT user_id FROM users")
            users: List[Tuple[int]] = cursor.fetchall()

            for user_tuple in users:
                user_id: int = user_tuple[0]

                cursor.execute("SELECT media_path, ad_text FROM ad")
                ad_info: Tuple[str, str] = cursor.fetchone()

                if ad_info:
                    media_path, ad_text = ad_info
                    await send_advertisement(user_id, media_path, ad_text, bot)
        await asyncio.sleep(SEND_INTERVAL_MIN)
