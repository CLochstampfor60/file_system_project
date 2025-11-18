#auth_server.py

# Step 3B: Authentication Server
# Handles user registration and login over encrypted network connection

import socket
import os

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encrypt(text, shift=3):
    pass


def caesar_encrypt(text, shift=3):
    pass

# ============================================================================
# NETWORK FUNCTIONS
# ============================================================================

def send_encrypted(sock, message):
    pass


def receive_encrypted(sock):
    pass

# ============================================================================
# USER MANAGEMENT (From auth_system.py)
# ============================================================================

def load_users():
    pass

def save_user(username, password):
    pass

def register_user(username, password):
    pass

def authenticate_user(username, password):
    pass

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