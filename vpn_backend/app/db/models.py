from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLAlchemy necesita una clase base para mapear las tablas.
Base = declarative_base()


class User(Base):
    """
    Modelo de la tabla 'users'.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # CAMPOS PARA WIREGUARD
    wg_public_key = Column(String, unique=True, nullable=True) # Clave pública del cliente
    wg_private_key = Column(String, unique=True, nullable=True) # Clave privada del cliente
    wg_ip_address = Column(String, unique=True, nullable=True) # La IP interna asignada (ej. 10.0.0.X)


class ConnectionLog(Base):
    """
    Modelo de la tabla 'connection_logs'.
    Almacena el historial de conexiones VPN.
    """
    __tablename__ = "connection_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ip_address = Column(String)
    connected_at = Column(DateTime, default=datetime.utcnow)
    disconnected_at = Column(DateTime, nullable=True)