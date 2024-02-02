from database.database import SQLiteDatabaseManager

class IsAdmin:
    def __init__(self, user_id):
        self.user_id = user_id

    def check_admin(self):
        try:
            with SQLiteDatabaseManager() as db:
                db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
                db.execute("SELECT 1 FROM admins WHERE user_id = ?", (self.user_id,))
                result = db.fetchone()
                return bool(result)
        except Exception as e:
            return False
