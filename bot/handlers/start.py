# Обработчики команды /start
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

async def start_command(message: types.Message):
    # Обработчик команды /start
    await message.answer("Привет! Это YLoader. Я готов к работе!")

    # Если нужно, можно добавить дополнительные действия, связанные с командой /start

# Регистрация обработчика команды /start
__all__ = ['start_command']
