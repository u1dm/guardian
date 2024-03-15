import sqlite3
from cryptography.fernet import Fernet


class Session:
    def __init__(self) -> None:
        self.__update_connection()
        self.__is_logined = False

        self.__execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            master_password TEXT NOT NULL,
            encryption_key TEXT NOT NULL
            )
            """)

    def login(self, username: str, master_password: str) -> str:
        self.__update_connection()
        self.__execute("SELECT * FROM Users WHERE username = ?", (username,))
        result = self.__cursor.fetchone()
        if result is not None:
            if result[2] == master_password:
                self.__encryption_key = result[3]
                self.__username = username
                self.__is_logined = True
                return "SUCCESS_LOGIN"
            else:
                "FAIL_LOGIN"
        else:
            return "FAIL_LOGIN"
            
    def register(self, username: str, master_password: str) -> None:
        self.__update_connection()
        self.__execute("SELECT * FROM Users WHERE username = ?", (username,))
        result = self.__cursor.fetchone()

        if result is None:
            key = Fernet.generate_key()
            self.__execute(
                "INSERT INTO Users (username, master_password, encryption_key) VALUES (?, ?, ?)",
                (username, master_password, key),
            )
            self.__execute(f"""
                CREATE TABLE IF NOT EXISTS {username} (
                id INTEGER PRIMARY KEY,
                label TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL
                )
                """)
            return "SUCCESS_REGISTER"
        else:
            return "USER_ALREADY_EXISTS"

    def add_password(self, label: str, login: str, password: str) -> None:
        if self.__is_logined:
            self.__update_connection()
            self.__execute(f"SELECT * FROM {self.__username} WHERE login = ?", (login,))
            data = self.__cursor.fetchone()
            if data is None:
                cipher = Fernet(self.__encryption_key)
                encrypted_password = cipher.encrypt(password.encode())
                self.__execute(
                    f"INSERT INTO {self.__username} (label, login, password) VALUES (?, ?, ?)",
                    (label, login, encrypted_password),
                )

    def get_password(self, label: str) -> str:
        if self.__is_logined:
            self.__update_connection()
            self.__execute(f"SELECT * FROM {self.__username} WHERE label = ?", (label,))
            data = self.__cursor.fetchone()
            if data:
                encrypted_password = data[3]
                cipher = Fernet(self.__encryption_key)
                decrypted_password = cipher.decrypt(encrypted_password).decode()
                return {'label': data[1], 'login': data[2], 'password': decrypted_password}
        
    def list_all_passwords(self) -> list:
        if self.__is_logined:
            self.__update_connection()
            result = []
            self.__execute(f"SELECT * FROM {self.__username}")
            for i in self.__cursor.fetchall():
                data = {'label': i[1], 'login': i[2], 'password': self.get_password(i[1])['password']}
                result.append(data)
            return result
        
    def delete_password(self, label: str) -> None:
        if self.__is_logined:
            self.__update_connection()
            self.__execute(f"DELETE FROM {self.__username} WHERE label = ?", (label,))  

    def __execute(self, command: str, *args) -> None:
        self.__cursor.execute(command, *args)
        self.__connection.commit()
    
    def __close(self) -> None:
        self.__connection.close()

    def __update_connection(self) -> None:
        self.__connection = sqlite3.connect("data.db")
        self.__cursor = self.__connection.cursor()
