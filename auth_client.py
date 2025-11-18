# auth_client.py

# Step 3B: Authentication Client
# Connects to authentication server for registration and login

import socket

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

def caesar_encypt(text, shift=3):
    pass

def caesar_decrypt(text, shift=3):
    # Decypts Ceasar cipher text.
    return caesar_encypt(text, -shift)

# ============================================================================
# NETWORK FUNCTIONS
# ============================================================================

def send_encrypted(sock, message):
    pass


def receive_encrypted(sock):
    pass


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def register(client_socket):
    pass

def login(client_socket):
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