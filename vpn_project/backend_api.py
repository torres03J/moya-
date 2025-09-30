import os
import subprocess
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- Configuración de la API ---
app = Flask(__name__)
API_KEY = os.getenv("API_SECRET_KEY")
CLIENT_CONFIG_PATH = os.path.join("config", "client.conf")

# --- Configuración de WireGuard ---
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")
CLIENT_PRIVATE_KEY = os.getenv("CLIENT_PRIVATE_KEY")
CLIENT_ADDRESS = os.getenv("CLIENT_ADDRESS")
ENDPOINT_IP = os.getenv("ENDPOINT_IP")
VPN_PORT = os.getenv("VPN_PORT")


# --- Funciones de Lógica de la VPN ---

def generate_client_config():
    """Genera el archivo .conf del cliente usando las variables de entorno."""
    
    config_content = f"""
[Interface]
PrivateKey = {CLIENT_PRIVATE_KEY}
Address = {CLIENT_ADDRESS}
DNS = 8.8.8.8

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {ENDPOINT_IP}:{VPN_PORT}
# Enrutamos TODO el tráfico por la VPN
AllowedIPs = 0.0.0.0/0, ::/0 
PersistentKeepalive = 25
"""
    os.makedirs(os.path.dirname(CLIENT_CONFIG_PATH), exist_ok=True)
    with open(CLIENT_CONFIG_PATH, "w") as f:
        f.write(config_content)
    
    print(f"[*] Archivo de configuración creado: {CLIENT_CONFIG_PATH}")
    return True

def run_wg_command(action):
    """Ejecuta los comandos de Docker y wg-quick."""
    
    # El servidor Docker solo se levanta/baja la primera vez o si hay cambios
    if action == "up":
        # Levantar el servidor Docker
        subprocess.run([f"sudo docker compose up -d", shell=True, check=True], check=True)
        print("[*] Servidor Docker WireGuard levantado.")
        
        # Activar la interfaz VPN en el host (donde corre el backend)
        subprocess.run(f"sudo wg-quick up {CLIENT_CONFIG_PATH}", shell=True, check=True)
        return "VPN activada."
    
    elif action == "down":
        # Desactivar la interfaz VPN
        subprocess.run(f"sudo wg-quick down {CLIENT_CONFIG_PATH}", shell=True, check=True)
        print("[*] Interfaz WireGuard desactivada.")
        
        # Bajar el servidor Docker (opcional, pero limpio)
        subprocess.run([f"sudo docker compose down", shell=True, check=True], check=True)
        return "VPN desactivada."
    
    return "Acción no válida."

# --- API Endpoints ---

@app.before_request
def check_auth():
    """Middleware simple para verificar la clave secreta en la cabecera."""
    if request.path in ['/activate', '/deactivate']:
        auth_key = request.headers.get('X-API-Key')
        if auth_key != API_KEY:
            return jsonify({"status": "error", "message": "Acceso no autorizado."}), 401

@app.route('/generate', methods=['POST'])
def generate_vpn():
    """Endpoint para generar el archivo de configuración del cliente."""
    if generate_client_config():
        return jsonify({"status": "success", "message": "Configuración generada. Lista para activar."})
    return jsonify({"status": "error", "message": "Fallo al generar la configuración."}), 500

@app.route('/activate', methods=['POST'])
def activate_vpn():
    """Endpoint llamado desde Vue.js para activar la VPN."""
    try:
        if not os.path.exists(CLIENT_CONFIG_PATH):
            generate_client_config()
            
        message = run_wg_command("up")
        return jsonify({"status": "success", "message": message})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al activar VPN: {e.stderr.decode()}"}), 500
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Asegúrate de tener Docker y wg-quick instalados."}), 500


@app.route('/deactivate', methods=['POST'])
def deactivate_vpn():
    """Endpoint llamado desde Vue.js para desactivar la VPN."""
    try:
        message = run_wg_command("down")
        return jsonify({"status": "success", "message": message})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error al desactivar VPN: {e.stderr.decode()}"}), 500


if __name__ == '__main__':
    # Genera la configuración del cliente al inicio si no existe
    if not os.path.exists(CLIENT_CONFIG_PATH):
         generate_client_config()
         
    # El puerto 5000 es el predeterminado de Flask
    app.run(host='0.0.0.0', port=8080)