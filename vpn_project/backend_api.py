import subprocess
import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# --- CONFIGURACIÓN Y LECTURA DE ENV ---
load_dotenv()
app = Flask(__name__)

# --- CONFIGURACIÓN ESTÁTICA ---
API_KEY = os.getenv("API_SECRET_KEY")
INTERFACE_NAME = "wg0" 
CONFIG_DIR = "config"
SERVER_CONF_PATH = os.path.join(CONFIG_DIR, "wg0.conf")

# Claves y Direcciones (Leídas del .env)
SERVER_PRIVATE_KEY = os.getenv("SERVER_PRIVATE_KEY")
CLIENT_PUBLIC_KEY = os.getenv("CLIENT_PUBLIC_KEY")
CLIENT_PRIVATE_KEY = os.getenv("CLIENT_PRIVATE_KEY")
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")
ENDPOINT_IP = os.getenv("ENDPOINT_IP")
VPN_PORT = os.getenv("VPN_PORT")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
CLIENT_ADDRESS = os.getenv("CLIENT_ADDRESS")


def generate_config_files():
    """Genera y guarda server.conf y client.conf."""
    
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        
    # --- Configuración del Servidor (Server.conf) ---
    # Incluye PostUp/PostDown para habilitar NAT y IP forwarding.
    # NOTA: Esto asume que la interfaz de salida de internet es 'eth0' (común en Linux/WSL).
    SERVER_CONFIG = f"""
[Interface]
PrivateKey = {SERVER_PRIVATE_KEY}
Address = {SERVER_ADDRESS}
ListenPort = {VPN_PORT}
PostUp = sysctl -w net.ipv4.ip_forward=1; iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0; iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = {CLIENT_PUBLIC_KEY}
AllowedIPs = {CLIENT_ADDRESS}
"""
    # --- Configuración del Cliente (Client.conf) ---
    CLIENT_CONFIG = f"""
[Interface]
PrivateKey = {CLIENT_PRIVATE_KEY}
Address = {CLIENT_ADDRESS}
DNS = 8.8.8.8, 8.8.4.4

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {ENDPOINT_IP}:{VPN_PORT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""

    with open(SERVER_CONF_PATH, "w") as f:
        f.write(SERVER_CONFIG.strip())
        
    with open(os.path.join(CONFIG_DIR, "client.conf"), "w") as f:
        f.write(CLIENT_CONFIG.strip())

    return SERVER_CONF_PATH


def run_wg_command(action):
    """Controla la interfaz WireGuard usando 'sudo wg-quick'."""
    
    if not os.path.exists(SERVER_CONF_PATH):
        generate_config_files()
        
    try:
        # Ejecutamos con 'sudo' para permisos de red.
        command = f"sudo wg-quick {action} {SERVER_CONF_PATH}"
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        if action == "up":
            return f"Túnel VPN activado con éxito. Interfaz {INTERFACE_NAME} arriba."
        if action == "down":
            return f"Túnel VPN desactivado con éxito. Interfaz {INTERFACE_NAME} abajo."
    
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        # Manejo de errores comunes (para no fallar si ya está activo/inactivo)
        if "Device or resource busy" in error_message and action == "up":
            raise Exception("Error: El túnel ya está activo. Intenta desactivar primero.")
        if "Cannot find device" in error_message and action == "down":
            return "El túnel ya estaba inactivo."
            
        # Si falla por permisos, será necesario ingresar la contraseña.
        if "Operation not permitted" in error_message:
            raise Exception("Error de permisos: Debes ingresar tu contraseña cuando el sistema la pida en la terminal de Flask.")
            
        raise Exception(f"Error de comando de VPN: {error_message}")

# --- RUTAS Y EJECUCIÓN ---

@app.before_request
def check_api_key():
    # Lógica de autenticación simple.
    if request.path.startswith('/activate') or request.path.startswith('/deactivate'):
        received_key = request.headers.get('X-API-Key')
        if received_key and received_key.strip() == API_KEY.strip():
            return 
        return jsonify({"status": "error", "message": "Acceso denegado"}), 403

@app.route("/")
def home():
    if not os.path.exists(SERVER_CONF_PATH):
        generate_config_files()
    return jsonify({"status": "ok", "message": "API VPN Server running locally. Config files generated."})

@app.route("/activate", methods=["POST"])
def activate():
    try:
        message = run_wg_command("up")
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error de activación: {e}"}), 500

@app.route("/deactivate", methods=["POST"])
def deactivate():
    try:
        message = run_wg_command("down")
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error de desactivación: {e}"}), 500

if __name__ == "__main__":
    print("Iniciando la generación de archivos de configuración...")
    try:
        generate_config_files()
        print(f"Archivos de configuración generados en la carpeta '{CONFIG_DIR}/'.")
    except Exception as e:
        print(f"ERROR al generar archivos: {e}")
        sys.exit(1)
        
    print("\nAPI de control VPN iniciada.")
    app.run(host='127.0.0.1', port=8080)