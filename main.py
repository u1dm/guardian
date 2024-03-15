from session import Session
import os
s = Session()

def clear_console():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)

def login():
    username = input("enter username: ")
    master_password = input("enter master password: ")
    login_state = s.login(username=username, master_password=master_password)
    if login_state == "SUCCESS_LOGIN":
        clear_console()
        print("You are successfully logined!")
        menu()
    elif login_state == "FAIL_LOGIN":
        clear_console()
        print("Wrong password or username! Try again.")
        login()


def register():
    username = input("enter username: ")
    master_password = input("enter master password: ")
    reg_state = s.register(username=username, master_password=master_password)
    if reg_state == "SUCCESS_REGISTER":
        clear_console()
        print("You are successfully registred!")
        s.login(username, master_password)
        menu()
    elif reg_state == "USER_ALREADY_EXISTS":
        clear_console()
        print("User already exists! Try again.")
        register()


def add_password():
    label = input("enter label: ")
    login = input("enter login: ")
    password = input("enter password: ")
    s.add_password(label=label, login=login, password=password)
    clear_console()


def get_password():
    label = input("enter label: ")
    item = s.get_password(label=label)
    if item is None:
        clear_console()
        print("No password with that label!")
        return
    max_label_length = len(item["label"])
    max_login_length = len(item["login"])
    max_password_length = len(item["password"])
    clear_console()
    print(
        f"{'Label':<{max_label_length}} {'Login':<{max_login_length}} {'Password':<{max_password_length}}"
    )

    print(
        f"{item['label']:<{max_label_length}} {item['login']:<{max_login_length}} {item['password']:<{max_password_length}}"
    )


def list_passwords():
    passwords = s.list_all_passwords()
    if passwords == []:
        clear_console()
        print('You have no passwords yet!')
        return
    max_label_length = max(len(item["label"]) for item in passwords)
    max_login_length = max(len(item["login"]) for item in passwords)
    max_password_length = max(len(item["password"]) for item in passwords)
    clear_console()
    print(
        f"{'Label':<{max_label_length}} {'Login':<{max_login_length}} {'Password':<{max_password_length}}"
    )

    for item in passwords:
        print(
            f"{item['label']:<{max_label_length}} {item['login']:<{max_login_length}} {item['password']:<{max_password_length}}"
        )


def delete_password():
    label = input("enter label: ")
    s.delete_password(label=label)
    clear_console()

def exit_program():
    clear_console()
    exit(0)

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
            exit_program()
        else:
            clear_console()
            print("Invalid choice. Please try again.")


def main():
    clear_console()
    print("1. Login")
    print("2. Register")

    choice = input("Enter your choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()
    else:
        clear_console()
        print("Invalid choice. Please try again.")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit_program()
