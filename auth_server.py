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
    pass

# ============================================================================
# MAIN SERVER
# ============================================================================


def main():
    
    def start_auth_server(host='127.0.0.1', port=5555):
        pass



if __name__ == "__main__":
    main()