from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from ..core.security import get_password_hash, verify_password
from ..services.firebase_service import verify_token
import json
import base64

# Crea un router para agrupar las rutas relacionadas.
router = APIRouter()

# Un modelo Pydantic para validar los datos de entrada


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    id_token: str


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Ruta para registrar un nuevo usuario.
    """
    # Verifica si el usuario ya existe.
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")

    # Hashea la contraseña y crea un nuevo usuario.
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(token: Token, db: Session = Depends(get_db)):
    """
    Ruta para autenticar un usuario con un token de Firebase.
    """
    # Verifica el token de Firebase.
    decoded_token = verify_token(token.id_token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token")

    # Busca el usuario en la base de datos local usando el UID de Firebase.
    uid = decoded_token.get("uid")
    # Nota: Aquí deberías buscar al usuario por el UID, no por el nombre.
    # Necesitarás agregar el UID como un campo en el modelo User en db/models.py

    # Para el ejemplo, asumiremos que el email de Firebase es el nombre de usuario
    username = decoded_token.get("email")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not find user in token")

    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found in database")

    return {"message": "Login successful"}

# Aquí agregarías más rutas para el control de la VPN, como:
# @router.post("/connect_vpn")
# def connect_vpn():
#    ...
