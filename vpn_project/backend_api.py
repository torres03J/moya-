import subprocess
import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# --- CONFIGURACIÓN DE LA API ---

# Cargar variables de entorno
load_dotenv()
app = Flask(__name__)

# Permite peticiones desde el puerto de desarrollo de Vue.js (cambia el puerto si es diferente)
# El asterisco "*" permite todos los orígenes, pero es más seguro especificar el de Vue.js.
CORS(app, 
    resources={r"/*": {
        "origins": [
            "http://localhost:5173", # Origen de Vue/Vite (cambia si usas otro puerto)
            "http://127.0.0.1:5173"
        ],
        "allow_headers": ["Content-Type", "X-API-Key"], # 🚨 CLAVE: Permitir X-API-Key
        "supports_credentials": True,
        "methods": ["GET", "POST", "OPTIONS"]
    }})  

# Asegúrate de que esta clave coincida con la de tu .env
API_KEY = os.getenv("API_SECRET_KEY")

# RUTA COMPLETA DE TAILSCALE EN WINDOWS
# Utilizamos la ruta estándar. Esto debe coincidir con tu instalación.
# NOTA: Si instalaste Tailscale en una ubicación diferente, debes cambiar esta línea.
TAILSCALE_EXECUTABLE = r"C:\Program Files\Tailscale\tailscale.exe"

# --- FUNCIÓN DE CONTROL DE TAILSCALE ---

def control_tailscale(action):
    """
    Controla la conexión de Tailscale en Windows. 
    Resuelve el problema de los espacios en la ruta usando comillas dobles.
    """
    
    # 1. Definir los comandos con comillas dobles alrededor del ejecutable
    # Esto soluciona el error de "C:\Program"
    if action == "up":
        # Sintaxis para el shell: "C:\ruta con espacios\tailscale.exe" up
        command = f'"{TAILSCALE_EXECUTABLE}" up --timeout 5s' 
        success_message = "VPN (Tailscale) activada con éxito."
    elif action == "down":
        # Sintaxis para el shell: "C:\ruta con espacios\tailscale.exe" down
        command = f'"{TAILSCALE_EXECUTABLE}" down'
        success_message = "VPN (Tailscale) desactivada con éxito."
    else:
        raise ValueError("Acción no válida. Use 'up' o 'down'.")

    print(f"Ejecutando comando en shell: {command}")
    
    try:
        # 2. Ejecutar el comando
        # shell=True permite que el subprocess interprete las comillas correctamente
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # 3. Manejo de mensajes (opcional)
        if action == "up" and ("already up" in result.stdout or "already running" in result.stdout):
             return "La VPN ya estaba activa."
        if action == "down" and "already down" in result.stdout:
             return "La VPN ya estaba inactiva."

        return success_message
    
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() or e.stdout.strip()
        
        # Si el ejecutable no se encuentra (aunque usamos la ruta completa)
        if "command not found" in error_message or "is not recognized" in error_message:
             raise Exception(f"Tailscale no está disponible en la ruta (PATH). Verifique la instalación o la ruta: {TAILSCALE_EXECUTABLE}")
            
        raise Exception(f"Error de comando Tailscale: {error_message}")

# --- RUTAS DE FLASK ---

@app.before_request
def check_api_key():
    """Verifica la clave API para todas las rutas de control, IGNORANDO OPTIONS."""
    
    # 🚨 CLAVE: Ignorar la verificación si el método es OPTIONS (requerido por CORS)
    if request.method == 'OPTIONS':
        return 
        
    if request.path == '/':
        return 
        
    received_key = request.headers.get('X-API-Key')
    if received_key and received_key.strip() == API_KEY.strip():
        return 
    
    # Si no es OPTIONS y falla la clave, devuelve 403
    return jsonify({"status": "error", "message": "Acceso denegado. Clave API incorrecta."}), 403

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Tailscale Control API está corriendo en Windows."})


@app.route("/activate", methods=["POST"])
def activate():
    """Ruta para activar la conexión de Tailscale (botón 'Conectar')."""
    try:
        message = control_tailscale("up")
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error de activación: {e}"}), 500

@app.route("/deactivate", methods=["POST"])
def deactivate():
    """Ruta para desactivar la conexión de Tailscale (botón 'Desconectar')."""
    try:
        message = control_tailscale("down")
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error de desactivación: {e}"}), 500

if __name__ == "__main__":
    print(f"API de control Tailscale iniciada en http://127.0.0.1:8080")
    # Usa threading=True para evitar bloqueos en entornos Windows de desarrollo
    app.run(host='127.0.0.1', port=8080)