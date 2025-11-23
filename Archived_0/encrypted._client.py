# encrypted_client.py
import socket

# Step 2C: Socket Client with Encryption
# Combines Caesar cipher with socket communication

# ============================================================================
# ENCRYPTION FUNCTIONS (from Step 1)
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
# NETWORK FUNCTIONS WITH ENCRYPTION
# ============================================================================

def send_encrypted(sock, message):
    # Encrypts a message and sends it over the socket.
    
    # Steps:
    # 1. Encrypt the message (string → encrypted string)
    # 2. Encode to bytes (encrypted string → bytes)
    # 3. Send over socket (bytes)

    encrypted = caesar_encrypt(message)
    sock.send(encrypted.encode('utf-8'))
    print(f"[ENCRYPTED] '{message}' → '{encrypted}'")


def receive_encrypted(sock):
    # Receives encrypted data and decrypts it.
    
    # Steps:
    # 1. Receive bytes from socket
    # 2. Decode to string (bytes → encrypted string)
    # 3. Decrypt (encrypted string → original string)

    encrypted_bytes = sock.recv(1024)
    encrypted = encrypted_bytes.decode('utf-8')
    decrypted = caesar_decrypt(encrypted)
    print(f"[DECRYPTED] '{encrypted}' → '{decrypted}'")
    return decrypted

# ============================================================================
# MAIN CLIENT
# ============================================================================

def start_encrypted_client():
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    host = '127.0.0.1'
    port = 5555

    print(f"[CONNECTING] Attempting to connect to {host}:{port}")
    client_socket.connect((host, port))
    print(f"[CONNECTED] Successfully connected to server!")

    # Send encrypted message
    message = "Hello from encrypted client!"
    print(f"\n[SENDING] Original message: {message}")
    send_encrypted(client_socket, message)

    # Receive encrypted response
    print(f"\n[RECEIVING] Waiting for server response")
    response = receive_encrypted(client_socket)
    print(f"[FINAL] Server's decrypted message: {response}")

    # Close connection
    client_socket.close()
    print(f"\n[CLOSED] Connection closed")


def main():
    print("="*60)
    print("ENCRYPTED SOCKET CLIENT")
    print("="*60)
    start_encrypted_client()


if __name__ == "__main__":
    main()