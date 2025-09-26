import subprocess
import os
import re

# ¡IMPORTANTE!: Estas rutas son estándar en Linux.
# Necesitas configurar tu servidor WireGuard en /etc/wireguard/wg0.conf en Linux/WSL
WIREGUARD_CONFIG_PATH = "/etc/wireguard/"
SERVER_CONFIG_FILE = "wg0.conf"

def generate_key_pair():
    """Genera un par de claves privada y pública para WireGuard."""
    try:
        # Genera la clave privada
        private_key = subprocess.run(
            ["wg", "genkey"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Genera la clave pública a partir de la privada
        public_key = subprocess.run(
            ["wg", "pubkey"],
            input=private_key,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        return private_key, public_key
    except FileNotFoundError:
        # Esto ocurrirá en Windows si no usas WSL
        print("ERROR: El comando 'wg' no fue encontrado. Asegúrate de tener WireGuard instalado en Linux/WSL.")
        return None, None
    except subprocess.CalledProcessError as e:
        print(f"Error al generar las claves de WireGuard: {e}")
        return None, None

def get_next_available_ip(used_ips: list) -> str:
    """Busca la próxima IP disponible en el rango 10.0.0.X."""
    base_ip = "10.0.0."
    for i in range(2, 255): # Empieza desde .2 para evitar conflictos.
        ip_candidate = f"{base_ip}{i}"
        if ip_candidate not in used_ips:
            return ip_candidate
    return None # No hay IPs disponibles

def add_peer_to_server(public_key: str, client_ip: str):
    """
    Añade un nuevo peer a la configuración del servidor de WireGuard usando 'sudo wg set'.
    REQUIERE PRIVILEGIOS DE ROOT (sudo) y LINUX.
    """
    try:
        # El comando 'wg' para añadir un peer sin reiniciar la interfaz
        subprocess.run(
            ["sudo", "wg", "set", "wg0", "peer", public_key, "allowed-ips", f"{client_ip}/32"],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al añadir peer a WireGuard: {e}")
        return False

def remove_peer_from_server(public_key: str):
    """
    Elimina un peer de la configuración del servidor de WireGuard.
    REQUIERE PRIVILEGIOS DE ROOT (sudo) y LINUX.
    """
    try:
        # El comando 'wg' para eliminar un peer
        subprocess.run(
            ["sudo", "wg", "set", "wg0", "peer", public_key, "remove"],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al eliminar peer de WireGuard: {e}")
        return False
        
def create_client_config(private_key: str, client_ip: str, server_public_key: str, server_ip: str) -> str:
    """
    Genera el archivo de configuración .conf para un cliente de WireGuard.
    """
    client_conf = f"""
[Interface]
PrivateKey = {private_key}
Address = {client_ip}/32
DNS = 8.8.8.8, 8.8.4.4
# PersistentKeepalive mantiene el túnel activo

[Peer]
PublicKey = {server_public_key}
Endpoint = {server_ip}:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
    return client_conf