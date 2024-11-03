import hashlib
import os

# File to store user data
USER_DATA_FILE = 'users.txt'


def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """Register a new user with a hashed password."""
    # Check if the user already exists
    if user_exists(username):
        print(f"User '{username}' already exists. Please choose a different username.")
        return False
    
    # Hash the password and store it
    hashed_password = hash_password(password)
    
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username}:{hashed_password}\n")
    
    print(f"User '{username}' registered successfully.")
    return True


def user_exists(username):
    """Check if a username already exists in the file."""
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            # Split the line safely, check for malformed data
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue  # Skip malformed lines
            
            stored_username, _ = parts
            if stored_username == username:
                return True
    return False


def login_user(username, password):
    """Log in a user by verifying their password."""
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False
    
    hashed_password = hash_password(password)
    
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username:
                if stored_password == hashed_password:
                    print(f"User '{username}' logged in successfully.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    
    print(f"User '{username}' not found.")
    return False


# Command-line interface to interact with the system
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()
