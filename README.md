# Secure File Sharing System

A secure file sharing system built with Python that implements encrypted client-server communication, user authentication, and isolated file storage.

## Project Information

**Course:**  CYSE 250 - Cybersecurity Programming and Networking, Old Dominion University (ODU)  
**Project Type:** Milestone Project  
**Date of Completion:** December 2025

## Overview

This project demonstrates fundamental cybersecurity concepts through a working file sharing system that features:

- **Encrypted Communication**: All network traffic protected using Caesar cipher encryption
- **User Authentication**: Secure registration and login system with persistent storage
- **File Operations**: Upload, download, list, and delete files
- **User Isolation**: Each user has private storage that other users cannot access
- **Socket Programming**: TCP client-server architecture on localhost

## Project Goals

### Security
Demonstrate core cybersecurity principles including:
- Message encryption/decryption during transmission
- User authentication and session management
- Data isolation and access control

### Educational
Provide hands-on experience with:
- Network programming using sockets
- Cryptographic algorithms (Caesar cipher)
- File management and I/O operations
- Client-server architecture

This project serves as a foundation for understanding production systems like Dropbox, Google Drive, and secure file transfer protocols.

## Features

### Core Functionality
- ✅ User registration with unique usernames
- ✅ User login with credential verification
- ✅ File upload with encryption
- ✅ File download with decryption
- ✅ File listing (user-specific)
- ✅ File deletion
- ✅ Secure logout

### Technical Features
- ✅ Caesar cipher encryption (shift=3) on all messages
- ✅ Two-way encryption display (client→server and server→client)
- ✅ TCP socket communication (port 5555)
- ✅ Persistent user storage in `users.txt`
- ✅ Isolated file directories per user
- ✅ Real-time encryption/decryption visualization
- ✅ Error handling and input validation
- ✅ Session management

## Requirements

### System Requirements
- Python 3.6 or higher
- Operating System: Windows, macOS, or Linux
- No external libraries required (uses Python standard library only)

### Python Modules Used
- `socket` - Network communication
- `os` - File system operations

## Quick Start

### 1. Start the Server
```bash
python auth_server.py
```

### 2. Start the Client (in new terminal)
```bash
python auth_client.py
```

### 3. Register and Login
- Choose option 2 to register
- Choose option 1 to login
- Upload/download files!

## File Structure

```
file_system_project/
├── auth_server.py          # Server application
├── auth_client.py          # Client application
├── README.md               # This file
├── users.txt               # User database (generated automatically)
└── server_files/           # File storage (generated automatically)
    ├── alice/              # User-specific directory
    ├── bob/                # User-specific directory
    └── ...                 # Additional user directories
```

## How It Works

### Encryption Process

All communication uses Caesar cipher with a shift of 3:

**Example: LOGIN command**
```
Original:  LOGIN|alice|secure123
Encrypted: ORJLQ|dolfh|vhfxuh123  ← Travels over network
Decrypted: LOGIN|alice|secure123  ← Server processes
```

**Server Display:**
```
[ENCRYPTED] ORJLQ|dolfh|vhfxuh123
[DECRYPTED] LOGIN|alice|secure123
------------------------------------------------------------
[ENCRYPTED REPLY] VXFFHVV|Orjlq vxffhvvixo.
[SENT] SUCCESS|Login successful.
```

This demonstrates encryption in **both directions** (client→server and server→client).

### Authentication Flow

1. **Registration:**
   - Client sends encrypted: `REGISTER|username|password`
   - Server checks if username exists
   - Saves to `users.txt` if available
   - Returns encrypted success/error message
   
<p align="center">
  <img src="Images\client_auth_starts.jpg" width="350" title="hover text">
</p>


2. **Login:**
   - Client sends encrypted: `LOGIN|username|password`
   - Server verifies credentials against `users.txt`
   - Establishes authenticated session if valid
   - Returns encrypted success/error message

### File Operations

1. **Upload:**
   - Client reads and encrypts file content
   - Sends `UPLOAD|filename|size` command
   - Transmits encrypted file data
   - Server decrypts and saves to user's directory

2. **Download:**
   - Client sends `DOWNLOAD|filename` command
   - Server encrypts file content
   - Sends encrypted data to client
   - Client decrypts and saves file

3. **List:**
   - Client sends `LIST` command
   - Server scans user's directory
   - Returns list of filenames

4. **Delete:**
   - Client sends `DELETE|filename` command
   - Server removes file from user's directory
   - Returns confirmation

## Code Requirements Met

This project satisfies all Milestone Project requirements:

- ✅ **Socket Programming** - TCP client-server architecture
- ✅ **Encryption/Decryption** - Caesar cipher on all communications (visible in both directions)
- ✅ **Authentication** - User registration and login system
- ✅ **Loops** - Server connection loop, menu loops, file transfer loops
- ✅ **Functions** - 20+ functions including encryption, networking, file operations
- ✅ **Lists** - File lists returned by `list_user_files()`
- ✅ **Dictionaries** - User dictionary from `load_users()`
- ✅ **Files** - `users.txt` for credentials, `server_files/` for uploads

## Key Functions

**Encryption Functions:**
- `caesar_encrypt(text, shift=3)` - Encrypts text using Caesar cipher
- `caesar_decrypt(text, shift=3)` - Decrypts Caesar cipher text

**Network Functions:**
- `send_encrypted(sock, message)` - Encrypts and sends messages (shows encrypted version)
- `receive_encrypted(sock)` - Receives and decrypts messages (shows both versions)

**Authentication Functions:**
- `load_users()` - Loads user database
- `save_user(username, password)` - Saves new user
- `register_user(username, password)` - Registers new user
- `authenticate_user(username, password)` - Verifies credentials

**File Management Functions:**
- `get_user_directory(username)` - Creates/returns user directory
- `list_user_files(username)` - Lists user's files
- `save_uploaded_file(username, filename, content)` - Saves uploaded file
- `get_file_content(username, filename)` - Retrieves file content
- `delete_user_file(username, filename)` - Deletes user's file

## Security Considerations

### Current Implementation (Educational)
- **Encryption:** Caesar cipher (shift=3)
- **Password Storage:** Plain text in `users.txt`
- **Transport:** Localhost only (127.0.0.1)

### Production Recommendations
For a production system, the following improvements would be necessary:

1. **Stronger Encryption:** Replace Caesar cipher with AES-256 or RSA
2. **Secure Password Storage:** Hash passwords using bcrypt or Argon2
3. **Network Security:** Implement SSL/TLS for network encryption
4. **Multi-threading:** Support multiple concurrent users
5. **Database:** Use SQLite or PostgreSQL instead of text files
6. **Password Management:** Allow users to change their passwords securely and implement secure password recovery mechanism.
7. **Admin User and Privileged Access:** Create separate admin role with elevated privileges

## File Type Support

### Current Support
- ✅ **Text files** (.txt, .py, .md, .csv, .json, etc.)
- ✅ Any UTF-8 encoded text content

### Not Currently Supported
- ❌ **Binary files** (.docx, .xlsx, .pdf, .jpg, .png, etc.)

**Why:** Caesar cipher is designed for text. Binary files would require Base64 encoding before encryption.

## Troubleshooting

### Server won't start
**Error:** `Address already in use`
- **Solution:** Port 5555 is in use. Close existing server or change port number.

### Client can't connect
**Error:** `Connection refused`
- **Solution:** Ensure server is running first on the same port.

### File upload fails
**Error:** `Could not read file`
- **Solution:** Check file path, ensure file exists, verify it's a text file.

## Technical Details

### Network Configuration
- **Protocol:** TCP
- **Host:** 127.0.0.1 (localhost)
- **Port:** 5555
- **Buffer Size:** 2048 bytes
- **Encoding:** UTF-8

### Caesar Cipher Details
- **Shift Amount:** 3
- **Preserves:** Letter case
- **Unchanged:** Numbers, symbols, spaces

**Example:**
```
A → D    a → d
LOGIN → ORJLQ
SUCCESS → VXFFHVV
```

## License

MIT License

Educational project for CYSE 250 - Cybersecurity Programming and Networking

---

