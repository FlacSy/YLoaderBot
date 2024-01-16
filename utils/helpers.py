# Вспомогательные функции
import logging
from aiogram import types
from aiogram.utils import executor
from config.secrets import ADMIN_ID
async def on_startup(dp):
    # Уведомление о запуске
    logging.warning('Starting...')

async def on_shutdown(dp):
    # Уведомление о завершении работы
    logging.warning('Shutting down...')

    # Закрытие соединений (если они есть)
    await dp.storage.close()
    await dp.storage.wait_closed()
