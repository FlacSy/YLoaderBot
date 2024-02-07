from database.database import SQLiteDatabaseManager
from typing import Union

class IsAdmin:
    def __init__(self, user_id: int):
        self.user_id: int = user_id

    def check_admin(self) -> bool:
        try:
            with SQLiteDatabaseManager() as db:
                db.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
                db.execute("SELECT 1 FROM admins WHERE user_id = ?", (self.user_id,))
                result: Union[None, tuple] = db.fetchone()
                return bool(result)
        except Exception as e:
            return False
