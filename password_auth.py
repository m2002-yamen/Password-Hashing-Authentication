import hashlib
import os

DATA_FILE = "users.txt"


def hash_password(password, salt):
    combined = password + salt
    return hashlib.sha256(combined.encode()).hexdigest()


def user_exists(username):
    if not os.path.exists(DATA_FILE):
        return False

    with open(DATA_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3 and parts[0] == username:
                return True

    return False


def register():
    print("\n--- USER REGISTRATION ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ")

    if user_exists(username):
        print("Registration failed: Username already exists.")
        return

    salt = os.urandom(16).hex()
    password_hash = hash_password(password, salt)

    with open(DATA_FILE, "a") as file:
        file.write(f"{username}:{salt}:{password_hash}\n")

    print("Registration successful.")
    print("Username:", username)
    print("Generated Salt:", salt)
    print("Password Hash:", password_hash)


def login():
    print("\n--- USER LOGIN ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ")

    if not os.path.exists(DATA_FILE):
        print("Login failed: No users registered.")
        return

    with open(DATA_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(":")

            if len(parts) != 3:
                continue

            stored_username, stored_salt, stored_hash = parts

            if stored_username == username:
                entered_hash = hash_password(password, stored_salt)

                if entered_hash == stored_hash:
                    print("Login successful.")
                    print("Password hash verification: MATCH")
                else:
                    print("Login failed: Incorrect password.")
                    print("Password hash verification: NO MATCH")

                return

    print("Login failed: Username not found.")


def main():
    while True:
        print("\n" + "=" * 50)
        print("PASSWORD HASHING AUTHENTICATION SYSTEM")
        print("=" * 50)
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()