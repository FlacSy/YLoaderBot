# Обработчики команды /help
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

async def help_command(message: types.Message):
    # Обработчик команды /help
    await message.answer("Это YLoader"
                         "Вот список доступных команд:\n"
                         "/start - начать работу с ботом\n"
                         "/help - получить справку о доступных командах")

    # Если нужно, можно добавить дополнительные действия, связанные с командой /help

# Регистрация обработчика команды /help
__all__ = ['help_command']
