"""
Configuración del proyecto Restaurante (ubicada en app/config.py)
Usa variables de entorno para sobreescribir valores por defecto.
"""
import os
from pathlib import Path

# Directorios base
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
ASSETS_DIR = PROJECT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
DATA_DIR = PROJECT_DIR / "data"

# Configuración de la base de datos MySQL
DB_CONFIG = {
	'host': os.getenv('DB_HOST', 'localhost'),
	'user': os.getenv('DB_USER', 'root'),
	'password': os.getenv('DB_PASSWORD', '12345678'),
	'database': os.getenv('DB_NAME', 'reserva_restaurante'),
}

# Rutas de iconos (puedes poner tus .ico en assets/icons)
ICONS_PATH = {
	'login': os.getenv('ICON_LOGIN', str(ICONS_DIR / 'login.ico')),
	'registro': os.getenv('ICON_REGISTRO', str(ICONS_DIR / 'registro.ico')),
	'admin': os.getenv('ICON_ADMIN', str(ICONS_DIR / 'admin.ico')),
	'cliente': os.getenv('ICON_CLIENTE', str(ICONS_DIR / 'cliente.ico')),
	'anadir_mesa': os.getenv('ICON_ANADIR_MESA', str(ICONS_DIR / 'anadir_mesa.ico')),
	'modificar_mesa': os.getenv('ICON_MODIFICAR_MESA', str(ICONS_DIR / 'modificar_mesa.ico')),
}

# Archivo de registro de usuarios (ruta absoluta dentro de data/)
REGISTRO_FILE = os.getenv('REGISTRO_FILE', str(DATA_DIR / 'users.txt'))
