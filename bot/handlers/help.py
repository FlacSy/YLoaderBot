from aiogram import types
from utils.is_admin import IsAdmin

async def user_commands() -> str:
    return (
        "\n\nВот список доступных команд:\n"
        "<i>/start</i> - начать работу с ботом\n\n"
        "<i>/help</i> - получить справку о доступных командах"
    )

async def admin_commands() -> str:
    return (
        "\n\n\n<b>Вот список доступных команд пользователей:</b>\n\n"
        "<i>/start</i> - начать работу с ботом\n\n"
        "<i>/help</i> - получить справку о доступных командах\n\n\n\n"
        "<b>Вот список доступных команд администраторов:</b>\n\n"
        "<i>/log</i> - для получения файла с логами\n\n"
        "<i>/ad_start</i> - для начала добавления рекламы\n\n"
        "<i>/cancel_ad</i> - для отмены начала добавления рекламы\n\n"
        "<i>/show_ad_list</i> - показывает список рекламы\n\n"
        "<i>/ad_state</i> - показывает включена ли реклама\n\n"
        "<i>/delete_ad</i> - удаление рекламы из списка"
    )

async def help_command(message: types.Message) -> None:
    user_id: int = message.from_user.id
    is_admin: bool = IsAdmin(user_id).check_admin()

    greeting: str = f"<b>Здравствуй, {message.from_user.first_name}, я YLoader</b>"

    if is_admin:
        admin_help: str = await admin_commands()
        await message.answer(f"{greeting}\n{admin_help}")
    else:
        user_help: str = await user_commands()
        await message.answer(f"{greeting}\n{user_help}")
