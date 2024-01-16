import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config.secrets import BOT_TOKEN
from bot.handlers import start, help
from utils import helpers
import datetime

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация логгера
log_file_path = os.path.join('logs', f'bot_log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')
logging.basicConfig(level=logging.INFO, filename=log_file_path, format='%(asctime)s - %(levelname)s - %(message)s')

# Логирование старта бота
logging.info('Bot has been started')

# Регистрация обработчиков команд
dp.register_message_handler(start.start_command, commands=['start'])
dp.register_message_handler(help.help_command, commands=['help'])

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=helpers.on_startup, on_shutdown=helpers.on_shutdown)
