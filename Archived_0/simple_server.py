#simple_server.py
import socket

# Step 2A: Simple Socket Server
# This server will:
# 1. Create a socket (like getting a phone)
# 2. Bind to an address and port (like choosing a phone number)
# 3. Listen for connections (like waiting for a call)
# 4. Accept a connection (like answering the phone)
# 5. Receive a message (like hearing what they say)
# 6. Send a response (like talking back)
# 7. Close the connection (like hanging up)

def start_simple_server():
    # Step 1: Create a socket
    # AF_INET = IPv4, SOCK_STREAM = TCP (reliable connection)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Bind to address and port
    host = '127.0.0.1'  # localhost (your own computer)
    port = 5555         # Port number (choose between 1024-65535)

    print(f"[SETUP] Creating server on {host}:{port}")
    server_socket.bind((host, port))

    # Step 3: Listen for connections
    # The number 1 means "queue up to 1 connection"
    server_socket.listen(1)
    print(f"[LISTENING] Server is waiting for connection...")

    # Step 4: Accept a connection  (this BLOCKS until someone connects)
    client_socket, client_address = server_socket.accept()
    print(f"[CONNECTED] Client connected from {client_address}")

    # Step 5: Receive data from client
    # 1024 = buffer size (max bytes to receive at once)
    message = client_socket.recv(1024).decode('utf-8')
    print(f"[RECEIVED] Client says: {message}")

    # Step 6: Send a response back'
    response = "Hello from the server! I got your message."
    client_socket.send(response.encode('utf-8'))
    print(f"[SENT] Sent response to client.")

    # Step 7: Close connections
    client_socket.close()
    server_socket.close()
    print(f"[CLOSED] Server shut down")

def main():
    print("=" * 50)
    print("Simple Socket Server")
    print("=" * 50)
    start_simple_server()

if __name__ == "__main__":
    main()