# utils/add_admin.py

## Модуль `add_admin.py`

Модуль `add_admin.py` содержит функции для управления списком администраторов бота в базе данных.

#### Основной функционал:

1. **Добавление администратора**: Функция `add_admin` добавляет пользователя с указанным `user_id` в таблицу администраторов, если его там еще нет.

#### Код модуля:

```python
from database.database import SQLiteDatabaseManager

def add_admin(user_id):
    # Добавление пользователя в таблицу администраторов
    try:
        with SQLiteDatabaseManager() as db:
            db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
            db.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
        print(f"User with ID {user_id} added as administrator.")
    except Exception as e:
        print(f"Error in add_admin: {e}")
```