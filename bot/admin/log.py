# Обработчики команды /log
import os
from aiogram import types
from aiogram.types import InputFile
from utils.is_admin import IsAdmin

async def log_command(message: types.Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin:    
        # Получение списка файлов в папке "logs"
        log_files = [f for f in os.listdir('logs') if os.path.isfile(os.path.join('logs', f))]
        
        # Проверка наличия файлов
        if log_files:
            # Сортировка файлов по дате последнего изменения
            log_files.sort(key=lambda x: os.path.getmtime(os.path.join('logs', x)), reverse=True)
            
            # Выбор последнего файла
            last_log_file = log_files[0]
            
            # Отправка файла пользователю
            with open(os.path.join('logs', last_log_file), 'rb') as log_file:
                await message.answer_document(log_file)
        else:
            await message.reply("В папке 'logs' нет файлов с логами.")

# Регистрация обработчика команды /help
__all__ = ['log_command']