from cryptography.fernet import Fernet
from app.core.config import settings
import base64

def get_fernet():
    key = settings.ENCRYPTION_KEY
    if not key or key == "TEMP_KEY_WILL_GENERATE_LATER":
        key = Fernet.generate_key().decode()

    if isinstance(key, str):
        key = key.encode()

    return Fernet(key)

def encrypt_token(token: str) -> str:
    if not token:
        return token

    fernet = get_fernet()
    encrypted = fernet.encrypt(token.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_token(encrypted_token: str) -> str:
    if not encrypted_token:
        return encrypted_token

    try:
        fernet = get_fernet()
        decoded = base64.urlsafe_b64decode(encrypted_token.encode())
        decrypted = fernet.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        print(f"Error decrypting token: {e}")
        return encrypted_token
