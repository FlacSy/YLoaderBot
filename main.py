import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor
from config.secrets import BOT_TOKEN
from bot.handlers import start, help, url
from bot.admin import log
from utils import helpers

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Логирование старта бота
logging.info('Bot has been started')

# Функция для регистрации обработчиков
async def register_handlers():
    dp.register_message_handler(start.start_command, commands=['start', 'about'])
    dp.register_message_handler(help.help_command, commands=['help', 'info'])
    dp.register_message_handler(log.log_command, commands=['log'])
    dp.register_message_handler(url.url_handler, content_types=types.ContentType.TEXT)
# Функция для запуска бота 
async def main():
    await register_handlers()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    executor.start_polling(dp, on_startup=helpers.on_startup, on_shutdown=helpers.on_shutdown)
