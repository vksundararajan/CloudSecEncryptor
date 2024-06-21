from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, file_path):
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data
