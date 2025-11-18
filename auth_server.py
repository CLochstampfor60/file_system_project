#auth_server.py

# Step 3B: Authentication Server
# Handles user registration and login over encrypted network connection

import socket
import os

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encrypt(text, shift=3):
    # Encrypts text using Ceasar cipher
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
    print(f"[SENT] {message}")

def receive_encrypted(sock):
    # Receives and decrypts a message from socket.
    encrypted_bytes = sock.recv(2048) # Increased buffer for longer messages.
    if not encrypted_bytes:
        return None
    encrypted = encrypted_bytes.decode('utf-8')
    decrypted = caesar_decrypt(encrypted)
    print(f"[RECEIVED] {decrypted}")
    return decrypted

# ============================================================================
# USER MANAGEMENT (From auth_system.py)
# ============================================================================

def load_users():
    # Loads users from users.txt file.
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    username, password = line.split('|', 1)
                    users[username] = password
    return users

def save_user(username, password):
    # Saves a new user to users.txt file.
    with open('users.txt', 'a') as f:
        f.write(f"{username}:{password}\n")

def register_user(username, password):
    # Registers a new user if username doesn't exist.
    users = load_users()

    if username in users:
        return False # Username takne
    save_user(username, password)
    return True

def authenticate_user(username, password):
    # Verifies if username and password match stored credentials.
    users = load_users()
    return username in users and users[username] == password

# ============================================================================
# CLIENT HANDLER
# ============================================================================

def handle_client(client_socket, client_address):
    # Handles the authentication requests from a connnected client.

    # Protocol:
    # - Client sends: REGISTER|username|password
    # - Server responds: SUCCESS or ERROR|message

    # - Client sends: LOGIN|username|password 
    # - Server responds: SUCCESS or ERROR|message

    print(f"[NEW CONNECTION] {client_address} connected.")

    authenticated = False
    current_user = None

    try:
        while True:
            # Receive encrypted command from client
            message = receive_encrypted(client_socket)
            if not message:
                break
            
            # Parse command (format: COMMAND|username|password)
            parts = message.split('|')
            command = parts[0]

            if command == "REGISTER":
                # Handle registration
                username = parts[1]
                password = parts[2]

                print(f"[REGISTER] Attempting to register user: {username}")

                if register_user(username, password):
                    send_encrypted(client_socket, "SUCCESS|Registration successful.")
                    print(f"[SUCCESS] User '{username}' registered.")
                else:
                    send_encrypted(client_socket, "ERROR|Username already exists.")
                    print(f"[ERROR] Username '{username}' already taken.")

            elif command == "LOGIN":
                # Handle login

                username = parts[1]
                password = parts[2]

                print(f"[LOGIN] Attempting to login for user: {username}")

                if authenticate_user(username, password):
                    authenticated = True
                    current_user = username
                    send_encrypted(client_socket, "SUCCESS|Login successful.")
                    print(f"[SUCCESS] User '{username}' logged in.")
                else:
                    send_encrypted(client_socket, "ERROR|Invalid username or password.")
                    print(f"[ERROR] Invalid credentials for '{username}'.")
            
            elif command == "LOGOUT":
                # Handle logout
                if authenticated:
                    print(f"[LOGOUT] User '{current_user} logged out.'")
                    authenticated = False
                    current_user = None
                    send_encrypted(client_socket, "SUCCESS|Logged out")
                else:
                    send_encrypted(client_socket, "ERROR|Not logged in")
            
            elif command == "EXIT":
                # Client wants to disconnect
                send_encrypted(client_socket, "ERROR|Unknown command")
    
    except Exception as e:
        print(f"[ERROR] Exception with {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected.")

# ============================================================================
# MAIN SERVER
# ============================================================================


def main():
    
    def start_auth_server(host='127.0.0.1', port=5555):
        # Starts the authentication server.
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind and listen
        server_socket.bind((host, port))
        server_socket.listen(5)

        print("=" * 60)
        print("AUTHENTICATION SERVER")
        print("=" * 60)
        print(f"[STARTING] Server starting {host}:{port}")
        print(f"[LISTENING] Waiting for connections...")
        print("=" * 60)

        try:
            while True:
                # Accept connection
                client_socket, client_address = server_socket.accept()
                handle_client(client_socket, client_address)
        
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Server shutting down...")
        
        finally:
            server_socket.close()
            print(f"[CLOSED] Server closed and offline.")
    
    start_auth_server()

if __name__ == "__main__":
    main()