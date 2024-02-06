# utils/is_admin.py

## Модуль `is_admin.py`

Модуль `is_admin.py` содержит класс `IsAdmin`, который предоставляет метод `check_admin` для проверки, является ли пользователь администратором бота.

#### Основной функционал:

1. **Проверка на администратора**: Метод `check_admin` возвращает `True`, если пользователь с `user_id` является администратором, и `False` в противном случае.

#### Код модуля:

```python
from database.database import SQLiteDatabaseManager

class IsAdmin:
    def __init__(self, user_id):
        self.user_id = user_id

    def check_admin(self):
        # Проверка, является ли пользователь администратором
        try:
            with SQLiteDatabaseManager() as db:
                db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
                db.execute("SELECT 1 FROM admins WHERE user_id = ?", (self.user_id,))
                result = db.fetchone()
                return bool(result)
        except Exception as e:
            return False
```