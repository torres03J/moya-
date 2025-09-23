from cryptography.fernet import Fernet
import bcrypt
from .config import settings

# Encriptación de datos


def encrypt_data(data: bytes) -> bytes:
    key = settings.SECRET_KEY.encode()
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(token: bytes) -> bytes:
    key = settings.SECRET_KEY.encode()
    f = Fernet(key)
    return f.decrypt(token)

# Hashing de contraseñas


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
