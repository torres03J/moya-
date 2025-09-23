import socket
import threading
import sys
import subprocess
from ..core.config import settings

# En una app real, la lógica de los túneles VPN es compleja.
# Aquí un ejemplo simplificado de un servidor de túnel.

# El puerto del túnel, diferente del puerto de la API si usas una.
TUNNEL_PORT = 65432


def handle_client(client_socket):
    """Maneja la conexión de un cliente en un hilo separado."""
    try:
        # Aquí iría la lógica de encriptación y desencriptación
        while True:
            # Recibe datos del cliente
            data = client_socket.recv(4096)
            if not data:
                break
            # Aquí se encripta, se envía al destino y se procesa la respuesta
            print(f"Recibidos {len(data)} bytes del cliente.")

    except Exception as e:
        print(f"Error en el manejo del cliente: {e}")
    finally:
        print("Cerrando la conexión del cliente.")
        client_socket.close()


def start_vpn_server():
    """Inicia el servidor VPN que escucha conexiones."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", TUNNEL_PORT))
    server.listen(5)
    print(f"Servidor VPN escuchando en el puerto {TUNNEL_PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión aceptada de {addr[0]}:{addr[1]}")
        # Inicia un hilo para manejar al cliente
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()

# --- Alternativa: Interacción con OpenVPN ---
# Si decides usar OpenVPN, esta sería otra forma de hacerlo:


def start_openvpn_server():
    """Inicia el servidor OpenVPN."""
    try:
        subprocess.run(["sudo", "openvpn", "--config",
                       "/ruta/a/tu/server.conf"], check=True)
    except FileNotFoundError:
        print("El comando 'openvpn' no fue encontrado. Asegúrate de tenerlo instalado.")
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar el servidor OpenVPN: {e}")
