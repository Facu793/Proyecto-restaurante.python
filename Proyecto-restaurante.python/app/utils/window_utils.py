"""
Utilidades para ventanas, incluyendo eliminación de iconos en Windows
"""
import sys
import os
import tkinter as tk
from pathlib import Path

def get_transparent_icon_path():
	"""Obtiene o crea la ruta al icono transparente"""
	try:
		from app.utils.create_transparent_icon import create_transparent_icon
		return create_transparent_icon()
	except:
		# Si no se puede crear, intentar usar uno existente
		icon_path = Path(__file__).parent.parent.parent / "assets" / "icons" / "transparent.ico"
		if icon_path.exists():
			return str(icon_path)
		return None

def remove_default_icon(window):
	"""
	Elimina el icono por defecto de Tkinter (pluma azul) en Windows usando API de Windows
	Usa múltiples métodos combinados para asegurar que funcione
	"""
	if sys.platform == 'win32':
		def _remove_icon():
			try:
				import ctypes
				from ctypes import wintypes
				
				# Forzar actualización para obtener el handle correcto
				window.update_idletasks()
				window.update()
				
				# Obtener el handle de la ventana
				hwnd = window.winfo_id()
				
				# Constantes de Windows API
				GCL_HICON = -14
				GCL_HICONSM = -34
				WM_SETICON = 0x0080
				ICON_SMALL = 0
				ICON_BIG = 1
				
				# Método 1: Usar SendMessage para establecer iconos a NULL
				try:
					SendMessageW = ctypes.windll.user32.SendMessageW
					SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
					SendMessageW.restype = wintypes.LRESULT
					
					# Establecer iconos a NULL (0)
					SendMessageW(hwnd, WM_SETICON, ICON_SMALL, 0)
					SendMessageW(hwnd, WM_SETICON, ICON_BIG, 0)
				except:
					try:
						ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, 0)
						ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, 0)
					except:
						pass
				
				# Método 2: Usar SetClassLongPtrW/SetClassLongW para eliminar iconos de la clase
				def is_64bit():
					return sys.maxsize > 2**32
				
				if is_64bit():
					try:
						ctypes.windll.user32.SetClassLongPtrW(hwnd, GCL_HICON, 0)
						ctypes.windll.user32.SetClassLongPtrW(hwnd, GCL_HICONSM, 0)
					except:
						pass
				else:
					try:
						ctypes.windll.user32.SetClassLongW(hwnd, GCL_HICON, 0)
						ctypes.windll.user32.SetClassLongW(hwnd, GCL_HICONSM, 0)
					except:
						pass
				
				# Método 3: Forzar redibujado de la ventana
				window.update_idletasks()
				window.update()
				
				# Método 4: Intentar invalidar la ventana para forzar actualización
				try:
					WM_SETICON = 0x0080
					InvalidateRect = ctypes.windll.user32.InvalidateRect
					InvalidateRect(hwnd, None, True)
				except:
					pass
					
			except ImportError:
				# Si ctypes no está disponible, usar método básico
				try:
					window.iconbitmap(default='')
					window.wm_iconbitmap(default='')
				except:
					pass
			except Exception:
				# Si todo falla, intentar método básico
				try:
					window.iconbitmap(default='')
					window.wm_iconbitmap(default='')
				except:
					pass
		
		# Método 5: Intentar usar un icono transparente como reemplazo
		# Esto es más confiable que intentar eliminar el icono
		def _set_transparent_icon():
			transparent_icon = get_transparent_icon_path()
			if transparent_icon and os.path.exists(transparent_icon):
				try:
					window.iconbitmap(transparent_icon)
					window.update_idletasks()
				except:
					pass
		
		# Intentar establecer el icono transparente inmediatamente y con delays
		_set_transparent_icon()
		window.after(50, _set_transparent_icon)
		window.after(150, _set_transparent_icon)
		
		# También ejecutar los métodos de eliminación
		window.after(50, _remove_icon)
		window.after(150, _remove_icon)
		window.after(300, _remove_icon)
		window.after(500, _remove_icon)
	else:
		# Para sistemas no-Windows
		try:
			window.iconbitmap(default='')
			window.wm_iconbitmap(default='')
		except:
			pass

