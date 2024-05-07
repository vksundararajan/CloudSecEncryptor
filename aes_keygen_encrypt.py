import os
from base64 import b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_aes_key_from_passphrase(passphrase, salt=None):
    """
    Generates a base64-encoded AES key from a passphrase using PBKDF2 HMAC for key derivation.
    """
    if salt is None:
        salt = os.urandom(16)  # Generate a random salt if not provided

    # Set up the key derivation function (KDF)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,                  # Output key will be 256 bits
        salt=salt,
        iterations=100000,          # High iteration count for security
        backend=None
    )

    key = kdf.derive(passphrase.encode())  # Derive key
    encoded_key = b64encode(key).decode('utf-8')
    encoded_salt = b64encode(salt).decode('utf-8')

    return encoded_key, encoded_salt

if __name__ == "__main__":
    passphrase = "YOUR_SECURE_PASSPHRASE"
    key, generated_salt = generate_aes_key_from_passphrase(passphrase)
    print("AES Key:", key)
    print("Salt:", generated_salt)
