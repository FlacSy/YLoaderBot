# Обработчики команды /help
from aiogram import types
from utils.is_admin import IsAdmin

async def help_command(message: types.Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    if is_admin:
        await message.answer(f"<b>Здраствуй, {message.from_user.first_name}, я YLoader</b>\n"
                            "Вот список доступных команд пользователей:\n"
                            "<i>/start</i> - начать работу с ботом\n"
                            "<i>/help</i> - получить справку о доступных командах\n\n"
                            "<b>Вот список доступных команд администратов:</b>\n"
                            "<i>/log</i> - для получения фала с логами\n"
                            "<i>/ad_start</i> - для начала добавления рекламы\n"
                            "<i>/cancel_ad</i> - для отмены начала добавления рекламы\n"
                            "<i>/show_ad_list</i> - показывает список рекламы\n"
                            "<i>/ad_state</i> - показывает включена ли реклама\n"
                            )
        
    else:
        await message.answer(f"<b>Здраствуй, {message.from_user.first_name}, я YLoader</b>"
                            "Вот список доступных команд:\n"
                            "<i>/start</i> - начать работу с ботом\n"
                            "<i>/help</i> - получить справку о доступных командах")


# Регистрация обработчика команды /help
__all__ = ['help_command']
