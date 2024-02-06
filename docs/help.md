# bot/handlers/help.md

## Модуль `help.py`

### Обработчик команды `/help`

Модуль `help.py` содержит обработчик команды `/help`, который активируется при вызове пользователем данной команды в чате с ботом.

#### Основной функционал:

1. **Справочная информация**: Бот отправляет пользователю сообщение с справочной информацией о доступных командах.

```python
from aiogram import types
from utils.is_admin import IsAdmin

async def user_commands() -> str:
    return (
        "Вот список доступных команд:\n"
        "<i>/start</i> - начать работу с ботом\n"
        "<i>/help</i> - получить справку о доступных командах"
    )

async def admin_commands() -> str:
    return (
        "Вот список доступных команд пользователей:\n"
        "<i>/start</i> - начать работу с ботом\n"
        "<i>/help</i> - получить справку о доступных командах\n\n"
        "<b>Вот список доступных команд администраторов:</b>\n"
        "<i>/log</i> - для получения файла с логами\n"
        "<i>/ad_start</i> - для начала добавления рекламы\n"
        "<i>/cancel_ad</i> - для отмены начала добавления рекламы\n"
        "<i>/show_ad_list</i> - показывает список рекламы\n"
        "<i>/ad_state</i> - показывает включена ли реклама\n"
        "<i>/delete_ad</i> - удаление рекламы из списка\n"
    )

async def help_command(message: types.Message):
    user_id = message.from_user.id
    is_admin = IsAdmin(user_id).check_admin()

    greeting = f"<b>Здравствуй, {message.from_user.first_name}, я YLoader</b>"

    if is_admin:
        admin_help = await admin_commands()
        await message.answer(f"{greeting}\n{admin_help}")
    else:
        user_help = await user_commands()
        await message.answer(f"{greeting}\n{user_help}")

# Регистрация обработчика команды /help
__all__ = ['help_command']
```

2. **Дополнительные действия**: По мере необходимости, в данном модуле могут быть добавлены дополнительные действия, связанные с командой `/help`.

### Использование:

- Пользователь вызывает команду `/help`.
- Бот отправляет сообщение с информацией о доступных командах.

```python
# Регистрация обработчика команды /help
dp.register_message_handler(help_command, commands=['help'])
``` 

Оба модуля `start.py` и `help.py` регистрируют свои обработчики команд в `main.py` с использованием библиотеки `aiogram`. При вызове соответствующих команд пользователем, соответствующие обработчики выполняют заданные действия и взаимодействуют с пользователем через сообщения.