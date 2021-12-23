import os
import hashlib
salt = os.urandom(32)
plaintext = 'hellow0rld'.encode()

digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000)
hex_hash = digest.hex()
print ("Hex Hash")
print(hex_hash)
byte_hash = digest.fromhex(digest.hex())
print ("Byte Hash")
print(byte_hash)
