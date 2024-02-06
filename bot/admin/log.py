import os
from aiogram import types
from config.settings import LOG_DIR
from utils.is_admin import IsAdmin

async def log_command(message: types.Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin:    
        # Получение списка файлов в папке "logs"
        log_files = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
        
        # Проверка наличия файлов
        if log_files:
            # Сортировка файлов по дате последнего изменения
            log_files.sort(key=lambda x: os.path.getmtime(os.path.join(LOG_DIR, x)), reverse=True)
            
            # Выбор последнего файла
            last_log_file = log_files[0]
            
            # Отправка файла пользователю
            with open(os.path.join(LOG_DIR, last_log_file), 'rb') as log_file:
                await message.answer_document(log_file)
        else:
            await message.reply(f"В папке {LOG_DIR} нет файлов с логами.")