import subprocess
import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import tempfile 

# Carga las variables de entorno (API_SECRET_KEY, claves, etc.)
load_dotenv()

app = Flask(__name__)
# Variables de la API
# USAMOS API_SECRET_KEY, que es la variable en tu .env
API_KEY = os.getenv("API_SECRET_KEY")
# Claves leídas directamente desde .env
SERVER_PRIVATE_KEY = os.getenv("SERVER_PRIVATE_KEY")
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")
CLIENT_PRIVATE_KEY = os.getenv("CLIENT_PRIVATE_KEY")
CLIENT_PUBLIC_KEY = os.getenv("CLIENT_PUBLIC_KEY")

# Nombre de la interfaz
INTERFACE_NAME = "wg0" 
ENDPOINT_PORT = 51820
SERVER_IP_CIDR = "10.0.0.1/24" # Dirección del servidor VPN

# ===============================================
# FUNCIONES DE CONFIGURACIÓN Y CONTROL DE WIREGUARD
# ===============================================

def generate_server_config():
    """Genera la cadena de configuración del servidor (wg0) con claves inyectadas."""
    
    # Versión limpia sin PostUp/PostDown que causaban problemas de permiso
    return f"""
[Interface]
PrivateKey = {SERVER_PRIVATE_KEY}
Address = {SERVER_IP_CIDR}
ListenPort = {ENDPOINT_PORT}

[Peer]
PublicKey = {CLIENT_PUBLIC_KEY}
AllowedIPs = 10.0.0.2/32
"""

def run_wg_command(action):
    """
    Controla la interfaz WireGuard usando comandos de bajo nivel (ip link, wg setconf) 
    para mayor estabilidad en entornos WSL/Virtualizados.
    """
    if action == "up":
        # 1. GENERAR ARCHIVO DE CONFIGURACIÓN TEMPORAL
        # Usamos suffix='.conf' y delete=False para que los comandos lo lean.
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as tmp_file:
            tmp_file.write(generate_server_config().strip())
            temp_config_path = tmp_file.name

        try:
            # Comando 1: Crear la interfaz (ip link add)
            subprocess.run(f"ip link add {INTERFACE_NAME} type wireguard", shell=True, check=True)
            
            # Comando 2: Cargar la configuración (wg setconf)
            # El comando 'wg setconf' lee la configuración del archivo temporal.
            subprocess.run(f"wg setconf {INTERFACE_NAME} {temp_config_path}", shell=True, check=True)
            
            # Comando 3: Asignar la IP y levantar la interfaz (ip address add & ip link set)
            subprocess.run(f"ip address add {SERVER_IP_CIDR} dev {INTERFACE_NAME}", shell=True, check=True)
            subprocess.run(f"ip link set up dev {INTERFACE_NAME}", shell=True, check=True)

            return f"VPN activada en interfaz {INTERFACE_NAME} usando comandos de bajo nivel."
        
        except subprocess.CalledProcessError as e:
            # Limpieza forzada si falla la activación (intenta borrar la interfaz si se creó parcialmente)
            subprocess.run(f"ip link delete {INTERFACE_NAME}", shell=True, check=False)
            raise Exception(f"Error en la secuencia de activación de bajo nivel: {e.stderr.strip() if e.stderr else e}")
        
        except Exception as e:
            raise Exception(f"Error desconocido en activación: {e}")
            
        finally:
            # 4. LIMPIEZA: Aseguramos la eliminación del archivo temporal
            os.remove(temp_config_path)

    elif action == "down":
        # Usamos el comando 'ip link delete' para eliminar la interfaz de red directamente, 
        # sin depender de wg-quick ni de archivos de configuración.
        command = f"ip link delete {INTERFACE_NAME}"
        
        # check=False es crucial para no fallar si la interfaz ya se ha eliminado.
        result = subprocess.run(command, shell=True, check=False, capture_output=True, text=True)

        # Verificamos si falló (returncode != 0)
        if result.returncode != 0:
            # Si el error es solo 'No such device', ignoramos el error, ya que la interfaz ya estaba abajo.
            if "No such device" in result.stderr:
                return f"VPN ya estaba desactivada o no encontrada ({INTERFACE_NAME})."
            else:
                # Si es un error real, lo volvemos a lanzar.
                raise Exception(f"Error desconocido al desactivar: {result.stderr.strip()}")

        return f"VPN desactivada en interfaz {INTERFACE_NAME}."
        
    return "Acción no válida."


# ===============================================
# RUTAS DE LA API Y AUTENTICACIÓN
# ===============================================

@app.before_request
def check_api_key():
    if request.path.startswith('/activate') or request.path.startswith('/deactivate'):
        # Limpiamos la clave recibida para evitar problemas con espacios en blanco.
        received_key = request.headers.get('X-API-Key')
        if received_key:
            received_key = received_key.strip()
        
        # Limpiamos la clave esperada (leída del .env) para evitar problemas con comillas o espacios.
        expected_key = API_KEY.strip().strip('"').strip("'")
        
        if received_key != expected_key:
            return jsonify({"status": "error", "message": "Acceso denegado"}), 403

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API VPN Server running locally."})

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
    # Importante: Debes correr el script con permisos de administrador (sudo) para usar comandos de red.
    if sys.platform != "win32" and os.geteuid() != 0:
        print("ERROR: Debes ejecutar este script con sudo/permisos de administrador (ej: sudo python3 backend_api.py)")
        sys.exit(1)
        
    app.run(host='0.0.0.0', port=8080)