from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from ..core.config import settings

# Crea la conexión a la base de datos usando la URL de PostgreSQL.
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_tables():
    """
    Crea todas las tablas definidas en 'models.py' en la base de datos.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Una función 'generadora' para obtener una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
