"""
Crea un icono transparente para usar en lugar del icono por defecto de Tkinter
"""
import os
from pathlib import Path

def create_transparent_icon():
	"""
	Crea un icono .ico transparente de 16x16 y 32x32 píxeles
	"""
	try:
		from PIL import Image, ImageDraw
	except ImportError:
		# Si PIL no está disponible, intentar crear el icono de otra manera
		return None
	
	# Directorio donde guardar el icono
	icon_dir = Path(__file__).parent.parent.parent / "assets" / "icons"
	icon_dir.mkdir(parents=True, exist_ok=True)
	icon_path = icon_dir / "transparent.ico"
	
	# Si ya existe, no recrearlo
	if icon_path.exists():
		return str(icon_path)
	
	try:
		# Crear imagen transparente de 16x16
		img16 = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
		
		# Crear imagen transparente de 32x32
		img32 = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
		
		# Guardar como .ico con múltiples tamaños
		img16.save(str(icon_path), format='ICO', sizes=[(16, 16), (32, 32)])
		
		return str(icon_path)
	except Exception as e:
		print(f"Error al crear icono transparente: {e}")
		return None

