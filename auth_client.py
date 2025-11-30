# auth_client.py

# Step 3B: Authentication Client
# Connects to authentication server for registration and login

import socket
import os

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
# FILE OPERATION FUNCTIONS (Add this entire section)
# ============================================================================

def upload_file(client_socket):
    # Handles file upload to server.
    # Flow:
    # 1. User enters file path
    # 2. Read file content
    # 3. Encrypt content
    # 4. Send UPLOAD command with filename and size
    # 5. Wait for READY signal
    # 6. Send encrypted file data
    # 7. Receive confirmation
    
    print("\n" + "=" * 60)
    print("UPLOAD FILE")
    print("=" * 60)

    filepath = input("Enter file path to upload (or press Enter to cancel): ").strip()

    if not filepath:
        print("[CANCELLED] Upload Cancelled")
        return

    # Check if file exists.
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found {filepath}.")
        return

    # Get just the filename (not full path)
    filename = os.path.basename(filepath)

    # Read file content
    try:
        with open(filepath, 'r') as f:
            file_content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return
    
    # Encrypt file content
    encrypted_content = caesar_encrypt(file_content)
    filesize = len(encrypted_content)

    # OPTIONAL FOR PRESENTATION PURPOSES ONLY!!!
    # Show encryption happening (in real-time)
    print(f"[INFO] File content encrypted ({len(file_content)} bytes → {filesize} bytes.)")

    # Send upload command: UPLOAD|filename|filesize
    message = f"UPLOAD|{filename}|{filesize}"
    send_encrypted(client_socket, message)

    # Wait for READY signal from server
    response = receive_encrypted(client_socket)

    if response == "READY":
        # Server is ready, sen encrypted file content
        client_socket.send(encrypted_content.encode('utf-8'))
        print(f"[SENDING] Uploading {filename}...")

        # Receive confirmation
        response = receive_encrypted(client_socket)
        parts = response.split('|', 1)

        if parts[0] == "SUCCESS": 
            print(f"[SUCCESS] {parts[1]}")
        else:
            print(f"[ERROR] {parts[1]}")

    else:
        print(f"[ERROR] Server not ready to receive file.")


def download_file(client_socket):
    # Handles file download from server.
    
    # Flow:
    # 1. User enters filename to download
    # 2. Send DOWNLOAD command
    # 3. Receive FILESIZE from server
    # 4. Send READY signal
    # 5. Receive encrypted file data
    # 6. Decrypt and save file
    # 7. Send confirmation

    print("\n" + "=" * 60)
    print("DOWNLOAD FILE")
    print("=" * 60)

    filename = input("Enter filename to download (or press Enter to cancel): ").strip()

    if not filename:
        print("[CANCELLED] Download cancelled.")
        return
    
    save_as = input(f"Save as (press Enter for '{filename}'): ").strip()
    if not save_as:
        save_as = filename
    
    # Send download command: DOWNLOAD|filename
    message = f"DOWNLOAD|{filename}"
    send_encrypted(client_socket, message)

    # Receive response (either FILESIZE or ERROR)
    response = receive_encrypted(client_socket)
    parts = response.split('|', 1)

    if parts[0] == "ERROR":
        print(f"[ERROR] {parts[1]}")
        return
    
    if parts[0] == "FILESIZE":
        filesize = int(parts[1])
        print(f"[RECEIVING] Downloading {filename} ({filesize} bytes...)")

        # Send READY signal to server
        send_encrypted(client_socket, "READY")

        # Receive encrypted file data in chunks
        received_data = b""
        remaining = filesize

        while remaining > 0:
            chunk_size = min(4096, remaining)
            chunk = client_socket.recv(chunk_size)
            if not chunk:
                break
            received_data += chunk
            remaining -= len(chunk)
        
        # Decrypt file content
        decrypted_content = caesar_decrypt(received_data.decode('utf-8'))

        # Save to file
        try:
            with open(save_as, 'w') as f:
                f.write(decrypted_content)

            # Save confirmation to server
            send_encrypted(client_socket, "RECEIVED")
            
            # Get final confirmation
            response = receive_encrypted(client_socket)
            parts = response.split('|', 1)

            if parts[0] == "SUCCESS":
                print(f"[SUCCESS] File saved as {save_as}")
            else:
                print(f"[ERROR] {parts[1]}")

        except Exception as e:
            print(f"[ERROR] Could not save file: {e}")

def list_files(client_socket):
    # Requests and displays list of files from server.
    
    # Flow:
    # 1. Send LIST command
    # 2. Receive list of files (separated by |)
    # 3. Display files

    print("\n" + "=" * 60)
    print("YOUR FILES")
    print("=" * 60)
    
    # Send list command
    send_encrypted(client_socket, "LIST")

    # Receive response: LIST|file1|file2|file3 or LIST|No files available 
    response = receive_encrypted(client_socket)
    parts = response.split('|')

    if parts[0] == "LIST":
        if len(parts) > 1 and parts[1] != "No file available":
            files = parts[1:] # Get all filenames after "LIST"
            for i, filename in enumerate(files, 1):
                print(f"{i}. {filename}")
        else:
            print("No files available")
    else:
        print(f"[ERROR] Unexpected response from server")    

    print("=" * 60)

def delete_file(client_socket):
    # Handles file deletion from server.
    
    # Flow:
    # 1. User enters filename to delete
    # 2. Confirm deletion
    # 3. Send DELETE command
    # 4. Receive confirmation

    print("\n" + "=" * 60)
    print("DELETE FILE")
    print("=" * 60)

    filename = input("Enter filename to delete (or press Enter to cancel)" ).strip()

    if not filename:
        print("[CANCELLED] Delete cancelled")
        return
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{filename}'? (yes/no): ").strip()

    if confirm != 'yes':
        print("[CANCELLED] File not deleted")
        return

    # Send delete command: DELETE|filename
    message = f"DELETE|{filename}"
    send_encrypted(client_socket, message)

    # Receive response
    response = receive_encrypted(client_socket)
    parts = response.split('|', 1)

    if parts[0] == "SUCCESS":
        print(f"[SUCCESS] {parts[1]}")
    else:
        print(f"[ERROR] {parts[1]}")


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

    while True:
        print("\n" + "=" * 60)
        print(f"WELCOME, {username.upper()}!")
        print("=" * 60)
        # print("You are now logged in.")
        # print("[FINISH THIS IN STEP 4] Add file operations here.")
        print("1. Upload File")
        print("2. Download File")
        print("3. List Files")
        print("4. Delete File")
        print("5. Logout")
        print("=" * 60)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            upload_file(client_socket)

        elif choice == '2':
            download_file(client_socket)

        elif choice == '3':
            list_files(client_socket)

        elif choice == '4':
            delete_file(client_socket)

        elif choice == '5':
            # Send logout request
            send_encrypted(client_socket, "LOGOUT")
            response = receive_encrypted(client_socket)
            print(f"\n[INFO] {response.split('|')[1] if '|' in response else response}")
            print("[GOODBYE] Logged out successfully!")
            break

        else:
            print("[ERROR] Invalid choice")

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
            print("SECURE FILE SHARING SYSTEM - CLIENT")
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