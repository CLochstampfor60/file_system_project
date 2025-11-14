# test_encryption.py

"""
Secure File Sharing System - Server
CYSE 250 Milestone Project
"""

import socket
import os
import json

def caesar_encrypt(text, shift=3):
    # Encrypts text using Caesar cipher with specified shift.
    # Only shifts alphabetic characters, preserves others.
    
    # How it works:
    # 1. Go through each character in the text
    # 2. If it's a letter, shift it by 'shift' positions
    # 3. If it's not a letter (space, number, etc.), keep it as-is
    # 4. Handle wrap-around (Z + 3 = C)

    result = ""

    for char in text:
        if char.isalpha():
             # Determine if uppercase or lowercase
            shift_base = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap around alphabet
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
             # Keep non-alphabetic characters unchanged
            result += char

    return result

def caesar_decrypt(text, shift=3):
    # Decrypts Caesar cipher text.

    return caesar_encrypt(text, -shift)



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
    print(f"Encrypted: Whvw 12345" )
    print()

    # Test 3: Encrypt then Decrypt
    print("# Test 3: Full Round Trip")
    original3 = "Secret Message 123"
    encrypted3 = caesar_encrypt(original3)
    decrypted3 = caesar_decrypt(encrypted3)

    print(f"Original:  {original3}")
    print(f"Encrypted: {encrypted3}")
    print(f"Decrypted: {decrypted3}")
    print(f"Match: {original3 == decrypted3}")  # Should be True!
    print()

if __name__ == "__main__":
    main()