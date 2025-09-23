import firebase_admin
from firebase_admin import credentials, auth
from ..core.config import settings
from firebase_admin.exceptions import FirebaseError


def initialize_firebase():
    """
    Inicializa la aplicación de Firebase si no ha sido inicializada.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)


def verify_token(id_token: str) -> dict:
    """
    Verifica el token de autenticación de Firebase.
    Retorna los datos del usuario si el token es válido.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except FirebaseError as e:
        # Aquí puedes manejar diferentes tipos de errores (token expirado, inválido, etc.)
        print(f"Firebase token verification failed: {e}")
        return None
