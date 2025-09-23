import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Configuración de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vpn.db")

    # Configuración de Firebase
    FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    # Clave de encriptación (¡IMPORTANTE: Usar una clave fuerte y secreta!)
    SECRET_KEY = os.getenv("SECRET_KEY")


settings = Settings()
