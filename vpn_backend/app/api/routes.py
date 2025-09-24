from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from ..core.security import get_password_hash
from ..services.firebase_service import verify_token
# Importa las nuevas funciones de WireGuard
from ..services.vpn_service import generate_key_pair, add_peer_to_server, remove_peer_from_server, create_client_config, get_server_public_key, get_next_available_ip

router = APIRouter()

# ... (El código de UserCreate, Token, register_user y login_user es el mismo) ...
from pydantic import BaseModel

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token")
    
    # Busca el usuario en la base de datos local usando el UID de Firebase.
    uid = decoded_token.get("uid")
    # Nota: Aquí deberías buscar al usuario por el UID, no por el nombre.
    
    # Para el ejemplo, asumiremos que el email de Firebase es el nombre de usuario
    username = decoded_token.get("email")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not find user in token")
        
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database")
        
    return {"message": "Login successful"}

@router.post("/vpn/connect")
def connect_vpn(token: Token, db: Session = Depends(get_db)):
    """
    Ruta para generar el archivo de configuración .conf para el cliente.
    """
    decoded_token = verify_token(token.id_token)
    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")
    
    # Obtener el usuario de la base de datos
    username = decoded_token.get("email")
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # 1. Si el usuario ya tiene una clave de WireGuard, usarla. Si no, generar un par de claves.
    if not db_user.wireguard_public_key:
        private_key, public_key = generate_key_pair()
        if not private_key:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate WireGuard keys.")
        
        # 2. Asignar una IP disponible
        used_ips = [user.wireguard_ip for user in db.query(User).all() if user.wireguard_ip]
        client_ip = get_next_available_ip(used_ips)
        if not client_ip:
            raise HTTPException(status_code=status.HTTP_507_INSUFFICIENT_STORAGE, detail="No available IP addresses.")
            
        # 3. Guardar la nueva clave y IP en la base de datos
        db_user.wireguard_public_key = public_key
        db_user.wireguard_ip = client_ip
        db.commit()
    else:
        # Si ya tiene una clave, usar la que ya existe.
        private_key = "TU_PRIVATE_KEY_GUARDADA_EN_UN_LUGAR_SEGURO" # Esta parte es más compleja y se podría gestionar con el token JWT
        public_key = db_user.wireguard_public_key
        client_ip = db_user.wireguard_ip
        
    # 4. Añadir el peer a la configuración del servidor de WireGuard.
    if not add_peer_to_server(public_key, f"{client_ip}/32"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add peer to WireGuard server.")
        
    # 5. Generar el archivo de configuración para el cliente.
    server_public_key = get_server_public_key()
    server_ip = "TU_IP_DEL_SERVIDOR_WG" # REEMPLAZAR con la IP pública de tu servidor
    
    client_config = create_client_config(private_key, client_ip, server_public_key, server_ip)

    # Retorna el archivo de configuración como una respuesta de descarga
    return Response(content=client_config, media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=client.conf"})

@router.post("/vpn/disconnect")
def disconnect_vpn(token: Token, db: Session = Depends(get_db)):
    """
    Ruta para revocar el acceso VPN.
    """
    decoded_token = verify_token(token.id_token)
    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")
    
    # 1. Busca la clave pública del usuario en la base de datos.
    username = decoded_token.get("email")
    db_user = db.query(User).filter(User.username == username).first()
    
    if db_user and db_user.wireguard_public_key:
        # 2. Elimina el peer del servidor de WireGuard.
        if not remove_peer_from_server(db_user.wireguard_public_key):
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove peer from WireGuard server.")

    return {"message": "VPN disconnected."}