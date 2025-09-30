## 🚀 Guía de Configuración del Backend VPN (Tailscale en Windows) ##

Esta guía documenta los pasos para configurar el servidor de control VPN usando Tailscale y Python/Flask en un entorno Windows.



Esta solución elimina problemas de permisos (sudo), conflictos de red y rutas de Linux (wg-quick).

# 1. Instalación y Configuración de Tailscale #

Tailscale debe instalarse en el dispositivo que ejecutará el backend (el "servidor" de control).



# 1.1. Registro e Instalación# 

Registro: Ve a https://tailscale.com/ y regístrate (Google, Microsoft, etc.) para crear tu red de malla privada.

Instalación: Descarga e instala la aplicación Tailscale para Windows.

Inicio de Sesión: Haz clic en el icono de Tailscale en la bandeja del sistema y selecciona "Log in", usando la misma cuenta del registro.

Verificación: Tu máquina aparecerá en el panel de administración de Tailscale con una IP que comienza con 100.x.x.x

# 1.2. Habilitar Ejecución de Scripts (PowerShell) #

Para permitir que el entorno virtual (venv) se active: 


Abre PowerShell como Administrador.

Ejecuta el siguiente comando (solo una vez):

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Escribe Y (Sí) y presiona Enter.

# 2. Configuración del Entorno Python #

 # 2.1. Entorno Virtual y Dependencias #

Navega a la carpeta raíz de tu proyecto en PowerShell:

python -m venv venv



.\venv\Scripts\Activate.ps1



pip install flask python-dotenv

# 2.2. Definición del Archivo .env # 

Crea o edita el archivo .env en la raíz del proyecto.



Esta es la clave que usarás en tus pruebas y en el frontend.



No uses comillas en el valor.

## Archivo: .env ## 

API_SECRET_KEY=ClaveVPNUni2025

# 3. Uso y Pruebas del Backend # 

Una vez que hayas copiado y guardado el código de la API de Flask (backend_api.py) en tu proyecto, usa los siguientes comandos en PowerShell.



# 3.1. Iniciar el Backend # 

python backend_api.py



# 3.2. Simulación del Botón "Conectar" (Activate) # 

Ejecuta el siguiente comando en PowerShell.



La clave (ClaveVPNUni2025) debe ir entre comillas.

$headers = @{"X-API-Key"="ClaveVPNUni2025"}



Invoke-WebRequest -Uri http://127.0.0.1:8080/activate -Method POST -Headers $headers

# 3.3. Simulación del Botón "Desconectar" (Deactivate) # 

$headers = @{"X-API-Key"="ClaveVPNUni2025"}



Invoke-WebRequest -Uri http://127.0.0.1:8080/deactivate -Method POST -Headers $headers

Con esto ya tienes un backend de control de VPN corriendo con Tailscale + Flask en Windows.

