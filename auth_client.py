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
    
    # Continue from this line...


    pass

# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def main_menu(client_socket):
    
    
    pass

def user_menu(client_socket, username):
    
    
    pass

# ============================================================================
# MAIN CLIENT
# ============================================================================

def main():
    
    def start_auth_client(host='127.0.0.1', port=5555):
        
        
        pass

    start_auth_client()
    pass

if __name__ == "__main__":
    main()