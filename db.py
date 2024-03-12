import sqlite3
from cryptography.fernet import Fernet


class DatabaseManager:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("data.db")
        self._cursor = self.connection.cursor()

        self.execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            master_password TEXT NOT NULL,
            encryption_key TEXT NOT NULL
            )
            """)

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def execute(self, command: str, *args) -> None:
        self.cursor.execute(command, *args)
        self.connection.commit()
    
    def close(self) -> None:
        self.connection.close()


db = DatabaseManager()
