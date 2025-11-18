# auth_client.py

# Step 3B: Authentication Client
# Connects to authentication server for registration and login

import socket

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encrypt(text, shift=3):
    # Encrypts text using Caesar cipher.
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    # Decrypts Caesar cipher text.
    return caesar_encrypt(text, -shift)

# ============================================================================
# NETWORK FUNCTIONS
# ============================================================================

def send_encrypted(sock, message):
    # Encrypts and sends a message over socket.
    encrypted = caesar_encrypt(message)
    sock.send(encrypted.encode('utf-8'))

def receive_encrypted(sock):
    # Receives and decrypts a message from socket.
    encrypted_bytes = sock.recv(2048)
    encrypted = encrypted_bytes.decode('utf-8')
    decrypted = caesar_decrypt(encrypted)
    return decrypted

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def register(client_socket):
    # Handles user registration with server.
    print("\n" + "=" * 60)
    print("USER REGISTRATION")
    print("=" * 60)

    username = input("Enter username (or press Enter to cancel): ").strip()
    if not username:
        print("[CANCELLED] Registration cancelled")
        return False
    
    password = input("Enter password (or press Enter to cancel): ").strip()
    if not password:
        print("[CANCELLED] Registration cancelled")
        return False
    
    # Send registration request to server
    message = f"REGISTER|{username}|{password}"
    send_encrypted(client_socket, message)

    # Receive response
    response = receive_encrypted(client_socket)
    parts = response.split('|', 1)

    if parts[0] == "SUCCESS":
        print(f"[SUCCESS] {parts[1]}")
        return True
    else:
        print(f"[ERROR] {parts[1]}")
        return False

def login(client_socket):
    # Handles user login with server.
    print("\n" + "=" * 60)
    print("LOGIN")
    print("=" * 60)

    username = input("Enter username (or press Enter to cancel): ").strip()
    if not username:
        print("[CANCELLED] Login cancelled.")
        return None
    
    password = input("Enter password (or press Enter to cancel): ").strip()
    if not password:
        print("[CANCELLED] Login cancelled.")
        return None
    
    # Send login request to server
    message = f"LOGIN|{username}|{password}"
    send_encrypted(client_socket, message)

    # Receive response
    response = receive_encrypted(client_socket)
    parts = response.split('|', 1)

    if parts[0] == "SUCCESS":
        print(f"[SUCCESS] {parts[1]}")
        return username
    else:
        print(f"[ERROR] {parts[1]}")
        return None

# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def main_menu(client_socket):
    # Main menu for login/register.
    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("=" * 60)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = login(client_socket)
            if username:
                return username # Successfully logged in

        elif choice == "2":
            register(client_socket)
        
        elif choice == "3":
            print("\n[GOODBYE] Exiting...")
            send_encrypted(client_socket, "EXIT")
            return None
        
        else:
            print("[ERROR] Invalid choice")

def user_menu(client_socket, username):
    # Menu after successful login.
    print("\n" + "=" * 60)
    print(f"WELCOME, {username}")
    print("=" * 60)
    print("You are not logged in.")
    print("[FINISH THIS IN STEP 4] Add file operations here.")
    print("=" * 60)

    input("\nPress Enter to logout...")

    # Send logout request
    send_encrypted(client_socket, "LOGOUT")
    response = receive_encrypted(client_socket)
    print(f"[INFO] {response.split('|')[1] if '|' in response else response}")


# ============================================================================
# MAIN CLIENT
# ============================================================================

def main():
    
    def start_auth_client(host='127.0.0.1', port=5555):
        # Starts in authentication client.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server
            print("=" * 60)
            print("AUTHENTICATION CLIENT")
            print("=" * 60)
            print(f"[CONNECTING] Connecting to {host}:{port}...")
            client_socket.connect((host, port))
            print(f"[CONNECTED] Connected to server!")
            
            # Show main menu (login/register)
            username = main_menu(client_socket)

            # If logged in, show user menu
            if username:
                user_menu(client_socket, username)

        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server. Is it running?")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            client_socket.close()
            print("[DISCONNECTED] Connection closed")
    
    start_auth_client()

if __name__ == "__main__":
    main()