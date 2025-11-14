"""
Secure File Sharing System - Server
CYSE 250 Milestone Project
"""

import socket
import os
import json

def caesar_encrypt(text, shift):
    return


def main():
    # Test 1: simple word
    original = 'Hello'
    encrypted = caesar_encrypt(original)
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Encrypted: Khoor" )
    print()

    # Test 2: with numbers and spaces
    original2 = "Test 12345"
    encrypted2 = caesar_encrypt(original2)
    print(f"Original: {original2}")
    print(f"Encrypted: {encrypted2}")
    print(f"Encrypted: Khoor" )
    print()

if __name__ == "__main__":
    main()