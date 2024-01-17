import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config.secrets import BOT_TOKEN
from bot.handlers import start, help
from bot.handlers import url
from utils import helpers

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Логирование старта бота
logging.info('Bot has been started')

# Регистрация обработчиков команд
dp.register_message_handler(start.start_command, commands=['start', 'about'])
dp.register_message_handler(help.help_command, commands=['help', 'info'])
dp.register_message_handler(url.url_handler, content_types=types.ContentType.TEXT)
# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=helpers.on_startup, on_shutdown=helpers.on_shutdown)
