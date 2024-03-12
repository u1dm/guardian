from session import Session
from db import db

s = Session()


def login():
    username = input("enter username: ")
    master_password = input("enter master password: ")
    login_state = s.login(username=username, master_password=master_password)
    if login_state == "SUCCESS_LOGIN":
        print("You are successfully logined!")
        menu()
    elif login_state == "FAIL_LOGIN":
        print("Wrong password or username! Try again.")
        login()


def register():
    username = input("enter username: ")
    master_password = input("enter master password: ")
    reg_state = s.register(username=username, master_password=master_password)
    if reg_state == "SUCCESS_REGISTER":
        print("You are successfully registred!")
        s.login(username, master_password)
        menu()
    elif reg_state == "USER_ALREADY_EXISTS":
        print("User already exists! Try again.")
        register()


def add_password():
    label = input("enter label: ")
    login = input("enter login: ")
    password = input("enter password: ")
    s.add_password(label=label, login=login, password=password)


def get_password():
    label = input("enter label: ")
    print(s.get_password(label=label))


def list_passwords():
    print(s.list_all_passwords())

def delete_password():
    label = input("enter label: ")
    s.delete_password(label=label)


def menu():
    while True:
        print("\nOptions:")
        print("1. Add a password")
        print("2. Get a password")
        print("3. List all passwords")
        print("4. Delete a password")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            get_password()
        elif choice == "3":
            list_passwords()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            db.close()
            exit(0)
        else:
            print("Invalid choice. Please try again.")


def main():
    print("1. Login")
    print("2. Register")

    choice = input("Enter your choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        db.close()
        exit(0)
