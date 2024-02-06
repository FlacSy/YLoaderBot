from database.database import SQLiteDatabaseManager

def add_admin(user_id):
    try:
        with SQLiteDatabaseManager() as db:
            db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
            db.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
        print(f"User with ID {user_id} added as administrator.")
    except Exception as e:
        print(f"Error in add_admin: {e}")