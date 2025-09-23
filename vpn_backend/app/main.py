from fastapi import FastAPI
import uvicorn
from .api.routes import router
from .db.database import create_db_tables
from .services.firebase_service import initialize_firebase
from .core.config import settings

# Crea la instancia principal de la aplicación FastAPI.
app = FastAPI(title="VPN Project Backend")

# Inicializa la base de datos al iniciar la aplicación.
create_db_tables()

# Inicializa la conexión con Firebase.
initialize_firebase()

# Incluye las rutas de la API.
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the VPN Backend API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
