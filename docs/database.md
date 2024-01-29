### Документация по database/database.py

#### Класс `SQLiteDatabaseManager`

```python
import sqlite3
import logging

class SQLiteDatabaseManager:
    def __init__(self, db_name="database/bot.db"):
        """
        Конструктор класса SQLiteDatabaseManager.

        Параметры:
            - db_name (str): Имя базы данных SQLite (по умолчанию: "database/bot.db").
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Метод, вызываемый при входе в контекст управления базой данных.

        Возвращает:
            - obj: Объект курсора для выполнения SQL-запросов.

        Исключения:
            - sqlite3.Error: В случае ошибки при подключении к базе данных.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Connected to the database: {self.db_name}")
            return self.cursor
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Метод, вызываемый при выходе из контекста управления базой данных.

        Параметры:
            - exc_type (type): Тип исключения (если есть).
            - exc_value (obj): Значение исключения (если есть).
            - traceback (obj): Объект трассировки (если есть).

        Возвращает:
            - bool: True, если исключение было обработано, False в противном случае.
        """
        if self.cursor:
            self.cursor.close()
            logging.info("Cursor closed")
        if self.conn:
            self.conn.commit()
            self.conn.close()
            logging.info("Connection closed")

        if exc_type is not None:
            logging.error(f"An error occurred: {exc_type}, {exc_value}")

        return False
```

#### Общая информация

- Класс `SQLiteDatabaseManager` предоставляет контекст управления базой данных SQLite.
- При входе в контекст устанавливается соединение с базой данных, и создается курсор для выполнения SQL-запросов.
- При выходе из контекста происходит закрытие курсора, фиксация изменений в базе данных и закрытие соединения.
- Логируются сообщения о подключении, закрытии и возможных ошибках при работе с базой данных.