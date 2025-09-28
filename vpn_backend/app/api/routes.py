from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from ..core.security import get_password_hash
from ..services.firebase_service import verify_token
# Importa las funciones de WireGuard
from ..services.vpn_service import (
    generate_key_pair, 
    add_peer_to_server, 
    remove_peer_from_server, 
    create_client_config, 
    get_next_available_ip
)

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
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

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
    decoded_token = verify_token(token.id_token)
    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token")
    
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
    Ruta para generar el archivo de configuración .conf para el cliente de WireGuard.
    """
    decoded_token = verify_token(token.id_token)
    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")
    
    username = decoded_token.get("email")
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # 1. Asignar claves y IP si no existen
    if not db_user.wg_public_key:
        private_key, public_key = generate_key_pair()
        if not private_key:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate WireGuard keys. Server issue.")

        # Obtener la próxima IP disponible
        used_ips = [user.wg_ip_address for user in db.query(User).all() if user.wg_ip_address]
        client_ip = get_next_available_ip(used_ips)
        if not client_ip:
            raise HTTPException(status_code=status.HTTP_507_INSUFFICIENT_STORAGE, detail="No available IP addresses.")

        # Guardar todo en la base de datos
        db_user.wg_public_key = public_key
        db_user.wg_private_key = private_key
        db_user.wg_ip_address = client_ip
        db.commit()

        # 2. **¡Paso Crítico de Linux!** Añade el peer a la configuración del servidor de WireGuard.
        if not add_peer_to_server(public_key, client_ip):
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add peer to WireGuard server. Check if you are running in Linux/WSL with sudo.")

    # 3. Usar los valores guardados
    private_key = db_user.wg_private_key
    public_key = db_user.wg_public_key
    client_ip = db_user.wg_ip_address
    
    # 4. Generar el archivo de configuración para el cliente.
    server_public_key = "vaVEwDDfPYafXQe+GfVhcv6yLGmtDEwqdyteBd1mLHo="
    server_ip = "192.168.160.1"
    
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
    
    username = decoded_token.get("email")
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not db_user.wg_public_key:
        return {"message": "User not connected or already disconnected."}

    public_key = db_user.wg_public_key

    # **¡Paso Crítico de Linux!** Eliminar el peer de la configuración del servidor de WireGuard.
    if not remove_peer_from_server(public_key):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove peer from WireGuard server. Check if you are running in Linux/WSL with sudo.")

    # Limpiar las claves de la base de datos
    db_user.wg_public_key = None
    db_user.wg_private_key = None
    db_user.wg_ip_address = None
    db.commit()

    return {"message": "VPN disconnected successfully."}