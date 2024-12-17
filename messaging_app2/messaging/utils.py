from cryptography.fernet import Fernet

SECRET_KEY = b'my_secret_key_for_fernet'  # Generate using Fernet.generate_key()

def encrypt_message(message):
    fernet = Fernet(SECRET_KEY)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    fernet = Fernet(SECRET_KEY)
    return fernet.decrypt(encrypted_message.encode()).decode()
