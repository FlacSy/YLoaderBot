import sqlite3
import logging
from typing import Optional, Any, ContextManager

class SQLiteDatabaseManager:
    def __init__(self, db_name: str = "database/bot.db"):
        self.db_name: str = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Connected to the database: {self.db_name}")
            return self.cursor
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type: Optional[type], exc_value: Optional[Exception], traceback: Any) -> bool:
        if self.cursor:
            self.cursor.close()
            logging.info("Cursor closed")
        if self.conn:
            try:
                self.conn.commit()
                logging.info("Changes committed to the database")
            except sqlite3.Error as commit_error:
                logging.error(f"Error committing changes to the database: {commit_error}")
            finally:
                self.conn.close()
                logging.info("Connection closed")

        if exc_type is not None:
            logging.error(f"An error occurred: {exc_type}, {exc_value}")

        return False
