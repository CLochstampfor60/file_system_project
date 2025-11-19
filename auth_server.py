#auth_server.py

# Step 3B: Authentication Server
# Handles user registration and login over encrypted network connection

import socket
import os

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encrypt(text, shift=3):
    # Encrypts text using Caesar cipher
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
        f.write(f"{username}|{password}\n")

def register_user(username, password):
    # Registers a new user if username doesn't exist.
    users = load_users()

    if username in users:
        return False # Username taken
    save_user(username, password)
    return True

def authenticate_user(username, password):
    # Verifies if username and password match stored credentials.
    users = load_users()
    return username in users and users[username] == password

# ============================================================================
# FILE MANAGEMENT FUNCTIONS
# ============================================================================

def get_user_dictionary(username):
    # Returns the directory path for a specific user.
    # Creates directory if it doesn't exist.
    user_dir = os.path.join('server_files', username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def list_user_files(username):
    # Returns a list of files in users' directory
    user_dir = get_user_dictionary(username)
    files = []
    if os.path.exists(user_dir):
        files = [f for f in os.listdir(user_dir)
                    if os.path.isfile(os.path.join(user_dir, f))
                 ]
    return files

def save_uploaded_files(username, filename, file_content):
    # Saves uploaded file content to user's dictionary.
    user_dir = get_user_dictionary(username)
    filepath = os.path.join(user_dir, filename)

    with open(filepath, 'w') as f:
        f.write(file_content)
    
    return True

def get_file_content(username, filename):
    # Reads and returns file content from user's dictionary.
    # Returns 'None' if file doesn't exist.
    user_dir = get_user_dictionary(username)
    filepath = os.path.join(user_dir, filename)

    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r') as f:
        content = f.read()

    return content

def delete_user_file(username, filename):
    # Deletes a file from user's dictionary.
    # Returns True if successful, False if file doesn't exist.

    user_dir = get_user_dictionary(username)
    filepath = os.path.join(user_dir, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False

# ============================================================================
# CLIENT HANDLER
# ============================================================================

def handle_client(client_socket, client_address):
    # Handles the authentication requests from a connected client.

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
                    print(f"[SUCCESS] User '{username}' registered.")   
                    send_encrypted(client_socket, "SUCCESS|Registration successful.")
                else:
                    print(f"[ERROR] Username '{username}' already taken.")
                    send_encrypted(client_socket, "ERROR|Username already exists.")


            elif command == "LOGIN":
                # Handle login

                username = parts[1]
                password = parts[2]

                print(f"[LOGIN] Attempting to login for user: {username}")

                if authenticate_user(username, password):
                    authenticated = True
                    current_user = username
                    print(f"[SUCCESS] User '{username}' logged in.")
                    send_encrypted(client_socket, "SUCCESS|Login successful.")
                else:
                    print(f"[ERROR] Invalid credentials for '{username}'.")
                    send_encrypted(client_socket, "ERROR|Invalid username or password.")
            
            elif command == "LOGOUT":
                # Handle logout
                if authenticated:
                    print(f"[LOGOUT] User '{current_user}' logged out.")
                    authenticated = False
                    current_user = None
                    send_encrypted(client_socket, "SUCCESS|Logged out")
                else:
                    send_encrypted(client_socket, "ERROR|Not logged in")
            
            elif command == "UPLOAD":
                # Handle file upload
                #  Format: UPLOAD|filename|filesize

                if not authenticated:
                    send_encrypted(client_socket, "ERROR|Please login first.")
                    continue

                filename = parts[1]
                filesize = int(parts[2])

                print(f"[UPLOAD] {current_user} uploading {filename} ({filesize} bytes.)")

                # Send ready signal
                send_encrypted(client_socket, "READY")

                # Receive file content
                file_content = ""
                remaining = filesize

                while remaining > 0:
                    chunk_size = min(4096, remaining)
                    chunk = client_socket.recv(chunk_size)
                    if not chunk:
                        break
                    # Decrypt the chunk
                    decrypted_chunk = caesar_decrypt(chunk.decode('utf-8'))
                    file_content = decrypted_chunk
                    remaining -= len(chunk)

                # Save file
                if save_uploaded_files(current_user, filename, file_content):
                    print(f"[SUCCESS] {filename} uploaded by {current_user}.")
                    send_encrypted(client_socket, "SUCCESS|File uploaded successfully!")
                else:
                    send_encrypted(client_socket, "ERROR|Failed to save file.")

            elif command == "DOWNLOAD":
                # Handle file download
                # Format: DOWNLOAD|filename

                

                pass

            elif command == "EXIT":
                # Client wants to disconnect
                send_encrypted(client_socket, "GOODBYE")
                break
    
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