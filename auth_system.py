# auth_system.py

# Step 3: User Authentication System
# Handles user registration and login with file storage
    
import os

# ============================================================================
# FILE OPERATIONS
# ============================================================================

def load_users():
    # Loads users from users.txt file.
    # Returns a dictionary: {username: password}
    
    # Example file content:
    # alice|password123
    # bob|secret456
    
    # Returns: {'alice': 'password123', 'bob': 'secret456'}

    users = {} # Start with empty dictionary

    # Check if file exists
    if os.path.exists('users.txt'): # Check if file exists
        with open('users.txt', 'r') as f: # Open for reading
            for line in f: # Read line by line
                line = line.strip() # Remove the whitespace/new lines
                if line and '|' in line: # Make sure line has data and separator
                    # Split on '|' to get username and password
                    username, password = line.split('|', 1)
                    users[username] = password # Add to dictionary
    return users

def save_user(username, password):
    # Saves a new user to users.txt file.
    # Appends to existing file (doesn't overwrite).
    
    # Format: username|password

    with open('users.txt', 'a') as f: # 'a' = append mode
        f.write(f"{username}|{password}")
    print(f"[SAVED] User '{username}' saved to file.")


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def register_user(username, password):
    # Registers a new user if username doesn't exist.
    
    # Returns:
    #     True if registration successful
    #     False if username already exists

    users = load_users() # Get existing users

    # Check if username already taken
    if username in users:
        print(f"[ERROR] Username '{username}' already exists! Please chooose a different one.")
        return False # Username taken!
    
    # Save new user
    save_user(username, password) # Save new user
    print(f"[SUCCESS] User '{username}' registered successfully!")
    return True

def authenticate_user(username, password):
    # Verifies if username and password match stored credentials.
    
    # Returns:
    #     True if credentials are valid
    #     False if invalid

    users = load_users()

    if username in users and users[username] == password:
        print(f"[SUCCESS] User '{username}' authenticated!")
        return True
    else:
        print(f"[ERROR] Invalid username and/or password! Please try again.")
        return False

# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_authentication():
    # Test the authentication system

    print("=" * 60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("=" * 60)

    # Test 1: Register new user
    print(f"\n--- Test 1: Register New User ---")
    register_user("alice", "pasword123")

    # Test 2: Try to register same user again (should fail)
    print(f"\n--- Test 2: Register Duplicate User ---")
    register_user("alice", "different_password")

    # Test 3: Register another user
    print(f"\n--- Test 3: Register Another User ---")
    register_user("bob", "secret456")

    # Test 4: Login with correct credentials
    print(f"\n--- Test 4: Login with Correct Credentials ---")
    register_user("alice", "pasword123")

    # Test 5: Login with wrong password
    print(f"\n--- Test 5: Login with Wrong Password ---")
    register_user("alice", "wrong_password")

    # Test 6: Login with non-existent user
    print(f"\n--- Test 6: Login with Non-existent User ---")
    authenticate_user("charlie", "wrong_password")

    # Test 7: Show all users
    print(f"\n--- Test 7: Display All Users---")
    users = load_users()
    print(f"Total users: {len(users)}")
    for username in users:
        print(f"  - {username}")


# ============================================================================
# INTERACTIVE MENU
# ============================================================================

def interactive_menu():
    # Interactive menu for testing authentication

    print("=" * 60)
    print("USER AUTHENTICATION SYSTEM")
    print("=" * 60)

    while True:
        print("\n" + "=" * 60)
        print("MENU")
        print("=" * 60)
        print("1. Register new user")
        print("2. Login")
        print("3. View all users")
        print("4. Exit")
        print("=" * 60)       

        choice = input("Enter choice: ").strip()

        if choice == '1':
            # Register
            print("\n--- REGISTER ---")
            username = input("Enter username: ").strip()
            password = input ("Enter password: ").strip()

            if not username or not password:
                print("[ERROR] Username and password cannot be empty!")
            else:
                register_user(username, password)
        
        elif choice == '2':
            #Login
            print("\n--- LOGIN ---")
            username = input("Enter username (or press 'Enter' to cancel): ").strip()

            # Check if user wants to cancel
            if not username:
                print("[CANCELED] Login cancelled.")
                continue

            password = input("Enter password (or press 'Enter' to cancel): ").strip()

            # Check if user wants to cancel
            if not password:
                print("[CANCELED] Login cancelled.")
                continue

            if authenticate_user(username, password):
                print(f"[SUCCESS] Welcome back, '{username}!'")
            else:
                print(f"[FAILED] Login failed! Please try again.")

        elif choice == '3':
            # View Users
            print("\n --- USERS ---")
            users = load_users()

            if users:
                for username, password in users.items():
                    print(f"Username: {username}, Password: {password}")
            else:
                print("No users registered yet in the database.")

        elif choice == '4':     
            # Exit
            print("\n [GOODBYE] Exiting program...")
            print("=" * 60)  
            break

        else:
            print("[ERROR] Invalid choice! Please try again using the options provided in the Menu.")



# ============================================================================
# MAIN
# ============================================================================

def main():
    # Choose which to run:

    # Option 1: Run automated tests
    # test_authentication()

    #Option 2: Run interactive menu
    interactive_menu()
    pass


if __name__ == "__main__":
    main()