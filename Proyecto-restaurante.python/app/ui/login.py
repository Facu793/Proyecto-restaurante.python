import tkinter as tk
from tkinter import messagebox
from app.ui.admin import MesasGUI
from app.ui.client import MesasClienteGUI
from app.config import DB_CONFIG
from app.ui.styles import COLORS, ICONS, FONTS, get_button_style, get_entry_style
from app.utils.window_utils import remove_default_icon
import mysql.connector


class LoginGUI:
	def __init__(self, master):
		self.master = master
		master.title("🍽️ Sistema de Gestión de Restaurante")
		master.geometry("450x550")
		master.configure(bg=COLORS['bg_main'])
		master.resizable(False, False)
		# Eliminar icono por defecto de Tkinter usando icono transparente
		from app.utils.window_utils import get_transparent_icon_path
		import os
		transparent_icon = get_transparent_icon_path()
		if transparent_icon and os.path.exists(transparent_icon):
			try:
				master.iconbitmap(transparent_icon)
			except:
				pass
		master.after(100, lambda: remove_default_icon(master))

		# Frame principal con padding
		self.main_frame = tk.Frame(master, bg=COLORS['bg_main'])
		self.main_frame.pack(fill='both', expand=True, padx=30, pady=30)

		# Título principal
		self.lbl_titulo = tk.Label(
			self.main_frame,
			text=f"{ICONS['restaurante']} Gestión de Restaurante",
			font=FONTS['title'],
			bg=COLORS['bg_main'],
			fg=COLORS['primary']
		)
		self.lbl_titulo.pack(pady=(0, 10))

		self.lbl_subtitulo = tk.Label(
			self.main_frame,
			text="Iniciar Sesión",
			font=FONTS['subtitle'],
			bg=COLORS['bg_main'],
			fg=COLORS['text_secondary']
		)
		self.lbl_subtitulo.pack(pady=(0, 30))

		# Frame para el formulario (card style)
		self.form_frame = tk.Frame(
			self.main_frame,
			bg=COLORS['bg_card'],
			relief='flat',
			bd=0
		)
		self.form_frame.pack(fill='both', expand=True, padx=20, pady=20)

		# Campo de usuario
		self.lbl_nombre = tk.Label(
			self.form_frame,
			text=f"{ICONS['usuario']} Nombre de usuario:",
			font=FONTS['body'],
			bg=COLORS['bg_card'],
			fg=COLORS['text_primary'],
			anchor='w'
		)
		self.lbl_nombre.pack(fill='x', padx=20, pady=(20, 5))

		self.entry_nombre = tk.Entry(
			self.form_frame,
			**get_entry_style(),
			width=30
		)
		self.entry_nombre.pack(fill='x', padx=20, pady=(0, 15))
		self.entry_nombre.bind('<Return>', lambda e: self.entry_contrasenia.focus())

		# Campo de contraseña
		self.lbl_contrasenia = tk.Label(
			self.form_frame,
			text=f"{ICONS['candado']} Contraseña:",
			font=FONTS['body'],
			bg=COLORS['bg_card'],
			fg=COLORS['text_primary'],
			anchor='w'
		)
		self.lbl_contrasenia.pack(fill='x', padx=20, pady=(0, 5))

		self.entry_contrasenia = tk.Entry(
			self.form_frame,
			**get_entry_style(),
			show="*",
			width=30
		)
		self.entry_contrasenia.pack(fill='x', padx=20, pady=(0, 25))
		self.entry_contrasenia.bind('<Return>', lambda e: self.inicio())

		# Frame para botones
		self.buttons_frame = tk.Frame(self.form_frame, bg=COLORS['bg_card'])
		self.buttons_frame.pack(fill='x', padx=20, pady=(0, 20))

		# Botón de inicio de sesión
		self.btn_inicio_sesion = tk.Button(
			self.buttons_frame,
			text=f"{ICONS['confirmar']} Iniciar sesión",
			command=self.inicio,
			**get_button_style(COLORS['success'], COLORS['hover_success'])
		)
		self.btn_inicio_sesion.pack(fill='x', pady=(0, 10))

		# Botón de registro
		self.btn_registro = tk.Button(
			self.buttons_frame,
			text=f"{ICONS['registro']} Registrarse",
			command=self.abrir_ventana_registro,
			**get_button_style(COLORS['secondary'], COLORS['hover_primary'])
		)
		self.btn_registro.pack(fill='x')

	def abrir_ventana_registro(self):
		self.registro_ventana = tk.Toplevel(self.master)
		self.registro_ventana.title("📝 Registro de Usuario")
		self.registro_ventana.geometry("450x600")
		self.registro_ventana.configure(bg=COLORS['bg_main'])
		self.registro_ventana.resizable(False, False)
		# Eliminar icono por defecto usando icono transparente
		from app.utils.window_utils import get_transparent_icon_path
		import os
		transparent_icon = get_transparent_icon_path()
		if transparent_icon and os.path.exists(transparent_icon):
			try:
				self.registro_ventana.iconbitmap(transparent_icon)
			except:
				pass
		self.registro_ventana.after(100, lambda: remove_default_icon(self.registro_ventana))

		# Frame principal
		main_reg_frame = tk.Frame(self.registro_ventana, bg=COLORS['bg_main'])
		main_reg_frame.pack(fill='both', expand=True, padx=30, pady=20)

		# Título
		titulo_reg = tk.Label(
			main_reg_frame,
			text=f"{ICONS['registro']} Crear Nueva Cuenta",
			font=FONTS['title'],
			bg=COLORS['bg_main'],
			fg=COLORS['primary']
		)
		titulo_reg.pack(pady=(0, 20))

		# Frame del formulario
		form_reg_frame = tk.Frame(main_reg_frame, bg=COLORS['bg_card'], relief='flat')
		form_reg_frame.pack(fill='both', expand=True, padx=15, pady=15)

		# Campos del formulario
		campos = [
			("Nombre de usuario", "entry_reg_nombre", ICONS['usuario']),
			("Apellido", "entry_reg_apellido", ICONS['usuario']),
			("Rol (Admin o Cliente)", "entry_reg_rol", ICONS['admin']),
			("Contraseña", "entry_reg_contrasenia", ICONS['candado']),
		]

		for i, (label_text, attr_name, icon) in enumerate(campos):
			label = tk.Label(
				form_reg_frame,
				text=f"{icon} {label_text}:",
				font=FONTS['body'],
				bg=COLORS['bg_card'],
				fg=COLORS['text_primary'],
				anchor='w'
			)
			label.grid(row=i*2, column=0, padx=20, pady=(15 if i == 0 else 10), sticky='w')

			entry = tk.Entry(form_reg_frame, **get_entry_style(), width=25)
			entry.grid(row=i*2+1, column=0, padx=20, pady=(0, 5), sticky='ew')
			setattr(self, attr_name, entry)

			if attr_name == "entry_reg_contrasenia":
				entry.config(show="*")

		# Campo de sexo
		sexo_label = tk.Label(
			form_reg_frame,
			text=f"{ICONS['usuario']} Sexo:",
			font=FONTS['body'],
			bg=COLORS['bg_card'],
			fg=COLORS['text_primary'],
			anchor='w'
		)
		sexo_label.grid(row=8, column=0, padx=20, pady=(10, 5), sticky='w')

		sexo_frame = tk.Frame(form_reg_frame, bg=COLORS['bg_card'])
		sexo_frame.grid(row=9, column=0, padx=20, pady=(0, 15), sticky='w')

		self.var_reg_sexo = tk.StringVar()
		self.rb_reg_masculino = tk.Radiobutton(
			sexo_frame,
			text="Masculino",
			variable=self.var_reg_sexo,
			value="Masculino",
			bg=COLORS['bg_card'],
			font=FONTS['body'],
			selectcolor=COLORS['secondary']
		)
		self.rb_reg_masculino.pack(side='left', padx=(0, 15))

		self.rb_reg_femenino = tk.Radiobutton(
			sexo_frame,
			text="Femenino",
			variable=self.var_reg_sexo,
			value="Femenino",
			bg=COLORS['bg_card'],
			font=FONTS['body'],
			selectcolor=COLORS['secondary']
		)
		self.rb_reg_femenino.pack(side='left')

		form_reg_frame.columnconfigure(0, weight=1)

		# Botón de registro
		self.btn_register = tk.Button(
			form_reg_frame,
			text=f"{ICONS['confirmar']} Registrarse",
			command=self.registro_usuario,
			**get_button_style(COLORS['success'], COLORS['hover_success'])
		)
		self.btn_register.grid(row=10, column=0, padx=20, pady=(10, 20), sticky='ew')

	def registro_usuario(self):
		primer_nombre = self.entry_reg_nombre.get()
		apellido = self.entry_reg_apellido.get()
		sexo = self.var_reg_sexo.get()
		contrasenia = self.entry_reg_contrasenia.get()
		rol = self.entry_reg_rol.get()

		if not primer_nombre or not apellido or not sexo or not contrasenia or not rol:
			messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
			return

		if rol not in ["Admin", "Cliente"]:
			messagebox.showwarning("Rol inválido", "El rol debe ser 'Admin' o 'Cliente'.")
			return

		try:
			conectar = mysql.connector.connect(**DB_CONFIG)
			cursor = conectar.cursor()

			cursor.execute("SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = %s", (primer_nombre,))
			if cursor.fetchone():
				messagebox.showerror("Error", "El nombre de usuario ya existe. Por favor, elija otro.")
				cursor.close()
				conectar.close()
				return

			query = "INSERT INTO usuarios (nombre_usuario, apellido, sexo, rol, contraseña) VALUES (%s, %s, %s, %s, %s)"
			cursor.execute(query, (primer_nombre, apellido, sexo, rol, contrasenia))
			conectar.commit()

			print(f"Usuario registrado: {primer_nombre} - Rol: {rol}")
			messagebox.showinfo("Registro exitoso", f"{ICONS['exito']} El usuario ha sido registrado con éxito en la base de datos.")
			cursor.close()
			conectar.close()
			self.registro_ventana.destroy()

		except mysql.connector.Error as err:
			messagebox.showerror("Error de base de datos", f"No se pudo registrar el usuario. Error: {err}")
			print(f"Error: {err}")

	def inicio(self):
		nombre = self.entry_nombre.get()
		contrasenia = self.entry_contrasenia.get()

		if not nombre or not contrasenia:
			messagebox.showwarning("Campos incompletos", "Por favor, ingrese nombre de usuario y contraseña.")
			return

		try:
			conectar = mysql.connector.connect(**DB_CONFIG)
			cursor = conectar.cursor()

			query = "SELECT nombre_usuario, contraseña, rol FROM usuarios WHERE nombre_usuario = %s"
			cursor.execute(query, (nombre,))
			usuario = cursor.fetchone()

			if usuario:
				nombre_db, contraseña_db, rol = usuario
				if contrasenia == contraseña_db:
					print(f"Inicio de sesión exitoso - Usuario: {nombre} - Rol: {rol}")
					
					if rol == "Admin":
						ventana_administrador_acceso = tk.Toplevel(self.master)
						MesasGUI(ventana_administrador_acceso)
					else:
						ventana_cliente_acceso = tk.Toplevel(self.master)
						MesasClienteGUI(ventana_cliente_acceso)
					
					self.entry_nombre.delete(0, tk.END)
					self.entry_contrasenia.delete(0, tk.END)
				else:
					messagebox.showerror("Error de inicio de sesión", f"{ICONS['error']} Contraseña incorrecta.")
			else:
				messagebox.showerror("Error de inicio de sesión", f"{ICONS['error']} Nombre de usuario o contraseña inválidos.")

			cursor.close()
			conectar.close()

		except mysql.connector.Error as err:
			messagebox.showerror("Error de base de datos", f"No se pudo conectar a la base de datos. Error: {err}")
			print(f"Error: {err}")
