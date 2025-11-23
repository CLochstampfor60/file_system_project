#simple_client.py

import socket

# Step 2B: Simple Socket Client
# This client will:
# 1. Create a socket (like getting a phone)
# 2. Connect to the server (like dialing a number)
# 3. Send a message (like talking)
# 4. Receive a response (like listening)
# 5. Close the connection (like hanging up)

def start_simple_client():

    # Step 1: Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Connect to the server
    host = '127.0.0.1'  # Server's address (localhost)
    port = 5555         # Server's port

    print(f"[CONNECTING] Attempting to connect to {host}:{port}")
    client_socket.connect((host, port))
    print(f"[CONNECTED] Successfully connected to server!")

    # Step 3: Send a message to the server
    message = "Hello, from the client!"
    client_socket.send(message.encode('utf-8'))
    print(f"[SENT] Sent message: {message}")

    # Step 4: Receive response from server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"[RECEIVED] Server says: {response}")

    # Step 5: Close the connection
    client_socket.close()
    print(f"[CLOSED] Connection closed.")


def main():
    print("="*50)
    print("SIMPLE SOCKET CLIENT")
    print("="*50)
    start_simple_client()


if __name__ == "__main__":
    main()