# encrypted_server.py

# Step 2C: Socket Server with Encryption
# Receives encrypted messages and sends encrypted responses

import socket
import time

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encrypt(text, shift=3):
    # Encrypts text using Ceasar cipher.
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
# NETWORK FUNCTIONS WITH ENCRYPTION
# ============================================================================

def send_encrypted(sock, message):
    # Encrypts a message and sends it.
    encrypted = caesar_encrypt(message)
    sock.send(encrypted.encode('utf-8'))
    print(f"[ENCRYPTED] '{message}'  → '{encrypted}'")

def receive_encrypted(sock):
    # Receives and decrypts a message.
    encrypted_bytes = sock.recv(1024)
    encrypted = encrypted_bytes.decode('utf-8')
    decrypted = caesar_decrypt(encrypted)
    print(f"[DECRYPTED] '{encrypted}'  → '{decrypted}'")
    return decrypted

# ============================================================================
# MAIN SERVER
# ============================================================================

def start_encrypted_server():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to address
    host = '127.0.0.1'
    port = 5555

    print(f"[SETUP] Creating server on {host}:{port}")
    server_socket.bind((host, port))

    # Listen for connections
    server_socket.listen(1)
    print(f"[LISTENING] Server is waiting for encrypted connection...")

    # Accept connection
    client_socket, client_address = server_socket.accept()
    print(f"[CONNECTED] Client connected from {client_address}")

    # Receive encrypted message
    print(f"\n[RECEIVING] Waiting for encrypted message...")
    message = receive_encrypted(client_socket)
    print(f"[FINAL] Client's decrypted message: {message}")

    # Send encrypted response
    response = "Hello, from encrypted server! Your message was received securely."
    print(f"\n[SENDING] Original response: {response}")
    send_encrypted(client_socket, response)

    # Give time for data to be sent
    time.sleep(0.5) # Wait half a second before closing

    # Close connections
    client_socket.close()
    server_socket.close()
    print(f"\n[CLOSED] Server shutdown or offline.")

def main():
    print("=" * 60)
    print("ENCRYPTED SOCKET SERVER")
    print("=" * 60)
    start_encrypted_server()

if __name__ == "__main__":
    main()