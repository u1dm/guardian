import sqlite3
import bcrypt
from cryptography.fernet import Fernet


class DatabaseManager:
    def __init__(self) -> None:
        self.__connection = sqlite3.connect("data.db")
        self.__cursor = self.__connection.cursor()

        self.__create_users_table()

    def __create_users_table(self) -> None:
        self.__execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            master_password TEXT NOT NULL,
            encryption_key TEXT NOT NULL
            )
            """)
        
    def create_user(self, username: str, master_password: str) -> bool:
        self.__execute('SELECT * FROM Users WHERE username = ?', (username,))
        result = self.__cursor.fetchone()

        if result is None:
            key = Fernet.generate_key()
            self.__execute('INSERT INTO Users (username, master_password, encryption_key) VALUES (?, ?, ?)', (username, master_password, key))
            self.__execute(f"""
                CREATE TABLE IF NOT EXISTS {username} (
                id INTEGER PRIMARY KEY,
                login TEXT NOT NULL,
                password TEXT NOT NULL
                )
                """)
            return True
        else:
            return False
        
    def login(self, username: str, master_password: str) -> bool:
        self.__execute('SELECT * FROM Users WHERE username = ?', (username,))
        result = self.__cursor.fetchone()
        if result is not None:
            if result[2] == master_password:
                return result[3]
        
    def add_user_password(self, username: str, master_password: str, login: str, password: str) -> bool:
        key = self.login(username, master_password)
        if key:
            self.__execute(f'SELECT * FROM {username} WHERE login = ?', (login,))
            data = self.__cursor.fetchone()
            if data is None:
                cipher = Fernet(key)
                encrypted_password = cipher.encrypt(password.encode())
                self.__execute(f'INSERT INTO {username} (login, password) VALUES (?, ?)', (login, encrypted_password))
                return True
            else:
                return False
                
    def get_user_password(self, username: str, master_password: str, login: str) -> bool:
        key = self.login(username, master_password)
        if key:
            self.__execute(f'SELECT * FROM {username} WHERE login = ?', (login,))
            data = self.__cursor.fetchone()
            if data:
                encrypted_password = data[2]
                cipher = Fernet(key)
                return cipher.decrypt(encrypted_password).decode()




    def __execute(self, command: str, *args) -> None:
        self.__cursor.execute(command, *args)
        self.__connection.commit()

    def close(self) -> None:
        self.__connection.close()
