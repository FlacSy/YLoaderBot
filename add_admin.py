from database.database import SQLiteDatabaseManager

def add_admin(user_id):
    try:
        with SQLiteDatabaseManager() as db:
            db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
            db.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
        print(f"User with ID {user_id} added as administrator.")
    except Exception as e:
        # Обработка ошибок, например, логирование
        print(f"Error in add_admin: {e}")

if __name__ == "__main__":
    try:
        user_id = int(input("Введите ID пользователя для добавления в администраторы: "))
        add_admin(user_id)
    except ValueError:
        print("Некорректный ввод ID пользователя. Введите целое число.")
