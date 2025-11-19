import tkinter as tk
import sys
from app.ui.login import LoginGUI
from app.utils.window_utils import remove_default_icon

if __name__ == "__main__":
	root = tk.Tk()
	
	# Eliminar icono por defecto de Tkinter en Windows usando API de Windows
	if sys.platform == 'win32':
		try:
			import ctypes
			# Obtener el handle de la ventana
			root.update_idletasks()
			hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
			# Obtener el handle de la ventana de forma más directa
			try:
				hwnd = root.winfo_id()
				# Intentar eliminar el icono usando SetClassLongPtr
				GCL_HICON = -14
				GCL_HICONSM = -34
				ctypes.windll.user32.SetClassLongPtrW(hwnd, GCL_HICON, 0)
				ctypes.windll.user32.SetClassLongPtrW(hwnd, GCL_HICONSM, 0)
			except:
				pass
		except Exception:
			# Si falla, intentar método alternativo
			try:
				root.iconbitmap(default='')
				root.wm_iconbitmap(default='')
			except:
				pass
	
	# Establecer icono transparente inmediatamente
	from app.utils.window_utils import get_transparent_icon_path
	import os
	transparent_icon = get_transparent_icon_path()
	if transparent_icon and os.path.exists(transparent_icon):
		try:
			root.iconbitmap(transparent_icon)
		except:
			pass
	
	login_gui = LoginGUI(root)
	# Eliminar icono también después de que se muestre la ventana
	root.after(200, lambda: remove_default_icon(root))
	root.mainloop()