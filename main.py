import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Import MemoryStorage
from config.secrets import BOT_TOKEN
from bot.handlers import start, help, url
from bot.admin import log, ad
from utils import helpers

# Initialize MemoryStorage
storage = MemoryStorage()

# Initialize bot and dispatcher with MemoryStorage
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Logging start of the bot
logging.info('Bot has been started')

# Function to register handlers
async def register_handlers():
    dp.register_message_handler(start.start_command, commands=['start', 'about'])
    dp.register_message_handler(help.help_command, commands=['help', 'info'])
    dp.register_message_handler(log.log_command, commands=['log'])
    dp.register_message_handler(ad.cmd_start_advertise, commands=['ad_start'])
    dp.register_message_handler(ad.cmd_cancel, commands=["cancel_ad"], state="*")
    dp.register_message_handler(ad.handle_media_content, content_types=types.ContentType.PHOTO, state=ad.AdvertiseStates.waiting_for_media) 
    dp.register_message_handler(ad.handle_ad_text, content_types=types.ContentType.TEXT, state=ad.AdvertiseStates.waiting_for_text)
    dp.register_message_handler(url.url_handler, content_types=types.ContentType.TEXT)

async def main():
    await register_handlers()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    executor.start_polling(dp, on_startup=helpers.on_startup, on_shutdown=helpers.on_shutdown)
