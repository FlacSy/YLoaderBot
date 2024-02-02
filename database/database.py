import sqlite3
import logging

class SQLiteDatabaseManager:
    def __init__(self, db_name="database/bot.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Connected to the database: {self.db_name}")
            return self.cursor
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
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
