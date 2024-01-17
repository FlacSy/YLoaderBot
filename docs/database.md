# database.py

## Модуль `database.py`

Модуль `database.py` предоставляет класс `SQLiteDatabaseManager` для управления подключением к SQLite базе данных. Этот класс реализует контекстный менеджер для удобства работы с базой данных.

### Основной функционал:

1. **Инициализация объекта:**
    - `__init__(self, db_name="database/bot.db")`: Конструктор класса, принимающий имя файла базы данных. По умолчанию используется файл "bot.db" в подпапке "database". Создает объект управления базой данных.

2. **Методы контекстного менеджера:**
    - `__enter__(self) -> sqlite3.Cursor`: Открывает подключение к базе данных и возвращает объект `sqlite3.Cursor`. Если подключение не установлено, генерирует ошибку и логирует соответствующее сообщение.
    - `__exit__(self, exc_type, exc_value, traceback) -> bool`: Завершает работу с базой данных, коммитит изменения, и закрывает соединение. В случае возникновения исключения, логирует сообщение об ошибке.

### Использование:

1. **Создание таблицы и вставка данных:**
    ```python
    with SQLiteDatabaseManager() as cursor:
        # Создаем таблицу, если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        
        # Вставляем данные в таблицу
        cursor.execute('''INSERT INTO users (name, age) VALUES (?, ?)''', ('John Doe', 25))
    ```

2. **Запрос данных из таблицы:**
    ```python
    with SQLiteDatabaseManager() as cursor:
        # Выполняем SQL-запрос
        cursor.execute("SELECT * FROM users")
        
        # Получаем все строки результата
        rows = cursor.fetchall()
        
        # Выводим результат
        for row in rows:
            print(row)
    ```

### Логирование:

- Логирование осуществляется с использованием модуля `logging`.
- Уровень логирования: INFO для успешных операций, ERROR для ошибок.

```python
# Пример конфигурации логирования
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```

### Замечания:

- В случае возникновения ошибок при подключении к базе данных, исключение `sqlite3.Error` будет сгенерировано, и соответствующее сообщение будет залогировано.