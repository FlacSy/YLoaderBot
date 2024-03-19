import os
from aiogram import types
from config.settings import LOG_DIR
from utils.is_admin import IsAdmin
from typing import List

async def log_command(message: types.Message) -> None:
    user_id: int = message.from_user.id
    is_admin: bool = IsAdmin(user_id).check_admin()

    if is_admin:    
        # Получение списка файлов в папке "logs"
        log_files: List[str] = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
        
        # Проверка наличия файлов
        if log_files:
            # Сортировка файлов по дате последнего изменения
            log_files.sort(key=lambda x: os.path.getmtime(os.path.join(LOG_DIR, x)), reverse=True)
            
            # Выбор последнего файла
            last_log_file: str = log_files[0]
            
            with open(os.path.join(LOG_DIR, last_log_file), 'r') as log_file:
                log_content = log_file.read()

            if len(log_content) <= 4000:
                await message.reply(f"```\n{log_content}\n```")
            else:
                with open(os.path.join(LOG_DIR, last_log_file), 'rb') as log_file:
                    await message.answer_document(log_file)
        else:
            await message.reply(f"В папке {LOG_DIR} нет файлов с логами.")
