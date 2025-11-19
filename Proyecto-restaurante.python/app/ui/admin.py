import tkinter as tk
from tkinter import messagebox
import mysql.connector
from app.config import DB_CONFIG
from app.ui.styles import COLORS, ICONS, FONTS, get_button_style, get_entry_style
from app.utils.window_utils import remove_default_icon

# Conexión a la base de datos
try:
	conectar = mysql.connector.connect(**DB_CONFIG)
	base_datos = conectar.cursor()
except mysql.connector.Error as err:
	print(f"Error al conectar a la base de datos: {err}")
	raise


class MesasGUI:
	def __init__(self, master):
		self.master = master
		master.title(f"{ICONS['admin']} Panel de Administración - Gestión de Mesas")
		master.geometry("1000x750")
		master.configure(bg=COLORS['bg_main'])
		# Eliminar icono por defecto usando icono transparente
		from app.utils.window_utils import get_transparent_icon_path
		import os
		transparent_icon = get_transparent_icon_path()
		if transparent_icon and os.path.exists(transparent_icon):
			try:
				master.iconbitmap(transparent_icon)
			except:
				pass
		master.after(100, lambda: remove_default_icon(master))

		# Header con título
		header = tk.Frame(master, bg=COLORS['primary'], height=60)
		header.pack(fill='x')
		header.pack_propagate(False)
		
		titulo = tk.Label(
			header,
			text=f"{ICONS['restaurante']} Gestión de Mesas - Administrador",
			font=FONTS['title'],
			bg=COLORS['primary'],
			fg=COLORS['text_light']
		)
		titulo.pack(pady=15)

		# Frame para las mesas
		self.frame_mesas = tk.Frame(master, bg=COLORS['bg_light'])
		self.frame_mesas.pack(fill='both', expand=True, padx=10, pady=10)

		# Frame para los botones en la parte inferior
		self.frame_botones = tk.Frame(master, bg=COLORS['bg_main'], height=100)
		self.frame_botones.pack(fill='x', padx=10, pady=(0, 10))
		self.frame_botones.pack_propagate(False)

		# Botones con mejor diseño
		self.btn_add_mesa = tk.Button(
			self.frame_botones,
			text=f"{ICONS['añadir']} Añadir Mesa",
			command=self.abrir_ventana_anadir_mesa,
			**get_button_style(COLORS['success'], COLORS['hover_success'])
		)
		self.btn_add_mesa.pack(side='left', padx=10, pady=15)

		self.btn_modificar_mesa = tk.Button(
			self.frame_botones,
			text=f"{ICONS['editar']} Modificar Mesa",
			command=self.abrir_ventana_modificar_mesa,
			**get_button_style(COLORS['warning'], COLORS['hover_warning'])
		)
		self.btn_modificar_mesa.pack(side='left', padx=10, pady=15)

		self.btn_delete_mesa = tk.Button(
			self.frame_botones,
			text=f"{ICONS['eliminar']} Eliminar Mesa",
			command=self.eliminar_mesa_seleccionada,
			**get_button_style(COLORS['danger'], COLORS['hover_danger'])
		)
		self.btn_delete_mesa.pack(side='left', padx=10, pady=15)

		# Lista para almacenar las mesas
		self.mesas = []
		self.mesa_seleccionada = None

		# Variables para mover mesas
		self.offset_x = 0
		self.offset_y = 0
		self.mesa_en_movimiento = False

		# Cargar las mesas existentes desde la base de datos
		self.cargar_mesas_desde_bd()

	def cargar_mesas_desde_bd(self):
		"""Carga las mesas almacenadas en la base de datos al inicio"""
		base_datos.execute("SELECT numero_mesa,nombre_cliente, ubicacion, estado, cantidad_personas FROM mesas")
		mesas_bd = base_datos.fetchall()

		for mesa_bd in mesas_bd:
			numero_mesa,nombre_cliente, ubicacion,estado_mesa, cantidad_personas = mesa_bd
			self.crear_mesa(numero_mesa,nombre_cliente, ubicacion,estado_mesa,cantidad_personas)

	def crear_mesa(self, numero_mesa,nombre_cliente,ubicacion_mesa,estado_mesa,capacidad):
		"""Crea una nueva mesa como botón y la coloca en el frame"""
		# Determinar color según estado
		estado_lower = estado_mesa.lower() if estado_mesa else "libre"
		if "libre" in estado_lower:
			mesa_color = COLORS['mesa_libre']
			estado_icon = "✅"
		elif "reservado" in estado_lower:
			mesa_color = COLORS['mesa_reservada']
			estado_icon = "🔴"
		else:
			mesa_color = COLORS['mesa_ocupada']
			estado_icon = "🟡"
		
		texto_mesa = f"{ICONS['mesa']} Mesa {numero_mesa}\n{ICONS['usuario']} {nombre_cliente or 'Sin cliente'}\n{ICONS['ubicacion']} {ubicacion_mesa}\n{estado_icon} {estado_mesa}\n{ICONS['personas']} {capacidad} personas"
		
		mesa_button = tk.Button(
			self.frame_mesas,
			text=texto_mesa,
			width=22,
			height=6,
			bg=mesa_color,
			fg=COLORS['text_light'],
			font=FONTS['body'],
			relief='raised',
			bd=2,
			cursor='hand2'
		)

		# Posicionar las mesas inicialmente
		x = (len(self.mesas) % 4) * 120 + 20
		y = (len(self.mesas) // 4) * 100 + 20
		mesa_button.place(x=x, y=y)

		# Bind de eventos para mover y seleccionar la mesa
		mesa_button.bind("<Button-1>", self.click_mesa)
		mesa_button.bind("<B1-Motion>", self.mover_mesa)
		mesa_button.bind("<ButtonRelease-1>", self.finalizar_mover_mesa)
		mesa_button.bind("<Double-Button-1>", self.seleccionar_mesa)  # Doble click para seleccionar

		# Añadir el botón a la lista de mesas
		self.mesas.append(mesa_button)

	def click_mesa(self, event):
		"""Maneja el click en la mesa - selecciona si no hay movimiento"""
		# Seleccionar la mesa primero
		if self.mesa_seleccionada and self.mesa_seleccionada != event.widget:
			# Restaurar color original de la mesa previamente seleccionada
			texto = self.mesa_seleccionada.cget("text")
			if "Libre" in texto or "libre" in texto:
				self.mesa_seleccionada.config(bg=COLORS['mesa_libre'])
			elif "Reservado" in texto or "reservado" in texto:
				self.mesa_seleccionada.config(bg=COLORS['mesa_reservada'])
			else:
				self.mesa_seleccionada.config(bg=COLORS['mesa_ocupada'])
			self.mesa_seleccionada.config(relief='raised', bd=2)

		# Seleccionar la nueva mesa
		self.mesa_seleccionada = event.widget
		self.mesa_seleccionada.config(bg=COLORS['mesa_seleccionada'], relief='solid', bd=3)
		
		# Preparar para mover (si se arrastra)
		self.offset_x = event.x
		self.offset_y = event.y
		self.mesa_en_movimiento = False

	def mover_mesa(self, event):
		"""Mueve la mesa seleccionada dentro del frame"""
		if self.mesa_seleccionada:
			self.mesa_en_movimiento = True
			x = event.x_root - self.frame_mesas.winfo_rootx() - self.offset_x
			y = event.y_root - self.frame_mesas.winfo_rooty() - self.offset_y
			self.mesa_seleccionada.place(x=x, y=y)

	def finalizar_mover_mesa(self, event):
		"""Finaliza el movimiento de la mesa"""
		# Si se movió, mantener seleccionada. Si no, ya está seleccionada por el click
		self.mesa_en_movimiento = False

	def seleccionar_mesa(self, event):
		"""Selecciona la mesa cuando se hace doble click (alternativa)"""
		# Este método es redundante ahora, pero lo mantenemos por compatibilidad
		event.widget.focus_set()

	def abrir_ventana_anadir_mesa(self):
		"""Abre una ventana emergente para añadir una nueva mesa con su número y capacidad"""
		self.ventana_anadir_mesa = tk.Toplevel(self.master)
		self.ventana_anadir_mesa.title(f"{ICONS['añadir']} Añadir Nueva Mesa")
		self.ventana_anadir_mesa.geometry("550x620")
		self.ventana_anadir_mesa.configure(bg=COLORS['bg_main'])
		self.ventana_anadir_mesa.resizable(True, True)
		self.ventana_anadir_mesa.minsize(550, 620)
		# Eliminar icono por defecto usando icono transparente
		from app.utils.window_utils import get_transparent_icon_path
		import os
		transparent_icon = get_transparent_icon_path()
		if transparent_icon and os.path.exists(transparent_icon):
			try:
				self.ventana_anadir_mesa.iconbitmap(transparent_icon)
			except:
				pass
		self.ventana_anadir_mesa.after(100, lambda: remove_default_icon(self.ventana_anadir_mesa))

		# Frame principal simple sin scroll - más directo
		main_frame = tk.Frame(self.ventana_anadir_mesa, bg=COLORS['bg_main'])
		main_frame.pack(fill='both', expand=True, padx=25, pady=20)

		titulo = tk.Label(
			main_frame,
			text=f"{ICONS['añadir']} Nueva Mesa",
			font=FONTS['title'],
			bg=COLORS['bg_main'],
			fg=COLORS['primary']
		)
		titulo.pack(pady=(0, 15))

		form_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief='flat')
		form_frame.pack(fill='both', expand=True, padx=15, pady=10)

		campos = [
			("Número de mesa", "entry_numero_mesa", ICONS['mesa']),
			("Nombre de cliente (opcional)", "entry_nombre_cliente", ICONS['usuario']),
			("Ubicación", "entry_ubicacion", ICONS['ubicacion']),
			("Estado (Libre/Reservado/Ocupado)", "entry_estado", "ℹ️"),
			("Cantidad de personas", "entry_capacidad_mesa", ICONS['personas']),
		]

		for i, (label_text, attr_name, icon) in enumerate(campos):
			label = tk.Label(
				form_frame,
				text=f"{icon} {label_text}:",
				font=FONTS['body'],
				bg=COLORS['bg_card'],
				fg=COLORS['text_primary'],
				anchor='w'
			)
			label.grid(row=i*2, column=0, padx=25, pady=(12 if i == 0 else 8), sticky='w')

			entry = tk.Entry(form_frame, **get_entry_style(), width=30)
			entry.grid(row=i*2+1, column=0, padx=25, pady=(0, 8), sticky='ew')
			setattr(self, attr_name, entry)

		form_frame.columnconfigure(0, weight=1)

		# Botón directamente en el form_frame
		btn_confirmar = tk.Button(
			form_frame,
			text=f"{ICONS['confirmar']} Añadir Mesa",
			command=self.anadir_mesa,
			**get_button_style(COLORS['success'], COLORS['hover_success'])
		)
		btn_confirmar.grid(row=10, column=0, padx=25, pady=(15, 20), sticky='ew')

	def anadir_mesa(self):
		"""Añade una nueva mesa con número personalizado y capacidad desde la ventana emergente"""
		numero_mesa = self.entry_numero_mesa.get().strip()
		nombre_cliente = self.entry_nombre_cliente.get().strip() or ""
		ubicacion_mesa = self.entry_ubicacion.get().strip()
		estado_mesa = self.entry_estado.get().strip() or "Libre"
		capacidad_mesa = self.entry_capacidad_mesa.get().strip()

		# Validaciones
		if not numero_mesa:
			messagebox.showwarning(f"{ICONS['warning']} Campo requerido", "Por favor, ingrese el número de mesa.")
			return
		
		if not numero_mesa.isdigit():
			messagebox.showwarning(f"{ICONS['warning']} Valor inválido", "El número de mesa debe ser un número.")
			return

		if not ubicacion_mesa:
			messagebox.showwarning(f"{ICONS['warning']} Campo requerido", "Por favor, ingrese la ubicación de la mesa.")
			return

		if not capacidad_mesa:
			messagebox.showwarning(f"{ICONS['warning']} Campo requerido", "Por favor, ingrese la cantidad de personas.")
			return
		
		if not capacidad_mesa.isdigit():
			messagebox.showwarning(f"{ICONS['warning']} Valor inválido", "La cantidad de personas debe ser un número.")
			return

		# Verificar si ya existe una mesa con ese número
		for mesa in self.mesas:
			if mesa.cget("text").startswith(f"🪑 Mesa {numero_mesa}"):
				messagebox.showerror(f"{ICONS['error']} Error", f"Ya existe una mesa con el número {numero_mesa}.")
				return

		# Crear la mesa en la interfaz
		self.crear_mesa(numero_mesa, nombre_cliente, ubicacion_mesa, estado_mesa, capacidad_mesa)

		# Insertar en la base de datos
		try:
			query = "INSERT INTO mesas (numero_mesa, nombre_cliente, ubicacion, estado, cantidad_personas) VALUES (%s, %s, %s, %s, %s);"
			valores = (numero_mesa, nombre_cliente if nombre_cliente else None, ubicacion_mesa, estado_mesa, capacidad_mesa)
			base_datos.execute(query, valores)
			conectar.commit()

			messagebox.showinfo(f"{ICONS['exito']} Éxito", f"La mesa {numero_mesa} ha sido añadida correctamente.")
			self.ventana_anadir_mesa.destroy()
		except mysql.connector.Error as err:
			messagebox.showerror(f"{ICONS['error']} Error de base de datos", f"No se pudo añadir la mesa. Error: {err}")

	def eliminar_mesa_seleccionada(self):
		"""Elimina la mesa seleccionada"""
		if self.mesa_seleccionada:
			respuesta = messagebox.askyesno("Eliminar Mesa",
											f"¿Estás seguro de eliminar {self.mesa_seleccionada.cget('text')}?")
			if respuesta:
				# Obtener el ID de la mesa a eliminar
				numero_mesa = self.mesa_seleccionada.cget("text").split("\n")[0].replace("🪑 Mesa ", "").strip()

				# Obtener el id_mesa a partir del numero_mesa
				query = "SELECT id_mesa FROM mesas WHERE numero_mesa = %s;"
				base_datos.execute(query, (numero_mesa,))
				resultado = base_datos.fetchone()

				if resultado:
					id_mesa = resultado[0]

					# Eliminar de la base de datos usando id_mesa
					query = "DELETE FROM mesas WHERE id_mesa = %s;"
					base_datos.execute(query, (id_mesa,))
					conectar.commit()

					# Actualizar la interfaz
					self.mesa_seleccionada.destroy()
					self.mesas.remove(self.mesa_seleccionada)
					self.mesa_seleccionada = None
				else:
					messagebox.showerror("Error", "No se encontró la mesa en la base de datos.")

	def abrir_ventana_modificar_mesa(self):
		"""Abre una ventana emergente para modificar la mesa seleccionada"""
		if not self.mesa_seleccionada:
			messagebox.showwarning("Sin selección", f"{ICONS['warning']} No has seleccionado ninguna mesa para modificar.")
			return

		self.ventana_modificar_mesa = tk.Toplevel(self.master)
		self.ventana_modificar_mesa.title(f"{ICONS['editar']} Modificar Mesa")
		self.ventana_modificar_mesa.geometry("450x500")
		self.ventana_modificar_mesa.configure(bg=COLORS['bg_main'])
		self.ventana_modificar_mesa.resizable(False, False)
		# Eliminar icono por defecto usando icono transparente
		from app.utils.window_utils import get_transparent_icon_path
		import os
		transparent_icon = get_transparent_icon_path()
		if transparent_icon and os.path.exists(transparent_icon):
			try:
				self.ventana_modificar_mesa.iconbitmap(transparent_icon)
			except:
				pass
		self.ventana_modificar_mesa.after(100, lambda: remove_default_icon(self.ventana_modificar_mesa))

		texto_mesa = self.mesa_seleccionada.cget("text")
		
		try:
			lineas = texto_mesa.split("\n")
			numero_actual = lineas[0].replace("🪑 Mesa ", "").strip()
			cliente_actual = lineas[1].replace("👤 ", "").strip() if len(lineas) > 1 else ""
			ubicacion_actual = lineas[2].replace("📍 ", "").strip() if len(lineas) > 2 else ""
			estado_actual = lineas[3].split(" ", 1)[1].strip() if len(lineas) > 3 else ""
			capacidad_actual = lineas[4].replace("👥 ", "").replace(" personas", "").strip() if len(lineas) > 4 else ""
		except (ValueError, IndexError):
			messagebox.showerror("Error", "El formato del texto de la mesa seleccionada no es el esperado.")
			return

		main_frame = tk.Frame(self.ventana_modificar_mesa, bg=COLORS['bg_main'])
		main_frame.pack(fill='both', expand=True, padx=30, pady=20)

		titulo = tk.Label(
			main_frame,
			text=f"{ICONS['editar']} Modificar Mesa",
			font=FONTS['title'],
			bg=COLORS['bg_main'],
			fg=COLORS['primary']
		)
		titulo.pack(pady=(0, 20))

		form_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief='flat')
		form_frame.pack(fill='both', expand=True, padx=15, pady=15)

		campos = [
			("Número de mesa", "entry_modificar_numero", ICONS['mesa'], numero_actual),
			("Nombre cliente", "entry_modificar_cliente", ICONS['usuario'], cliente_actual),
			("Ubicación", "entry_modificar_ubicacion", ICONS['ubicacion'], ubicacion_actual),
			("Estado (Libre/Reservado/Ocupado)", "entry_modificar_estado", "ℹ️", estado_actual),
			("Capacidad de personas", "entry_modificar_capacidad", ICONS['personas'], capacidad_actual),
		]

		for i, (label_text, attr_name, icon, valor_actual) in enumerate(campos):
			label = tk.Label(
				form_frame,
				text=f"{icon} {label_text}:",
				font=FONTS['body'],
				bg=COLORS['bg_card'],
				fg=COLORS['text_primary'],
				anchor='w'
			)
			label.grid(row=i*2, column=0, padx=20, pady=(15 if i == 0 else 10), sticky='w')

			entry = tk.Entry(form_frame, **get_entry_style(), width=25)
			entry.grid(row=i*2+1, column=0, padx=20, pady=(0, 5), sticky='ew')
			entry.insert(0, valor_actual)
			setattr(self, attr_name, entry)

		form_frame.columnconfigure(0, weight=1)

		btn_confirmar = tk.Button(
			form_frame,
			text=f"{ICONS['confirmar']} Guardar Cambios",
			command=self.modificar_mesa,
			**get_button_style(COLORS['warning'], COLORS['hover_warning'])
		)
		btn_confirmar.grid(row=10, column=0, padx=20, pady=(15, 20), sticky='ew')

	def modificar_mesa(self):
		"""Modifica el número, cliente, ubicación, estado y la capacidad de la mesa seleccionada"""
		nuevo_numero = self.entry_modificar_numero.get()
		nuevo_cliente = self.entry_modificar_cliente.get()
		nueva_ubicacion = self.entry_modificar_ubicacion.get()
		nuevo_estado_mesa = self.entry_modificar_estado.get()
		nueva_capacidad = self.entry_modificar_capacidad.get()

		if nuevo_numero and nuevo_numero.isdigit() and nueva_capacidad and nueva_capacidad.isdigit():
			# Verificar que no haya otra mesa con el mismo número
			for mesa in self.mesas:
				if mesa != self.mesa_seleccionada and mesa.cget("text").startswith(f"🪑 Mesa {nuevo_numero}"):
					messagebox.showerror(f"{ICONS['error']} Error", f"Ya existe una mesa con el número {nuevo_numero}.")
					return

			# Obtener el id_mesa actual en lugar de usar numero_actual
			numero_actual = self.mesa_seleccionada.cget("text").split("\n")[0].replace("🪑 Mesa ", "").strip()
			query_id = "SELECT id_mesa FROM mesas WHERE numero_mesa = %s;"
			base_datos.execute(query_id, (numero_actual,))
			resultado = base_datos.fetchone()

			if resultado:
				id_mesa = resultado[0]

				# Actualizar en la base de datos usando id_mesa
				query = "UPDATE mesas SET numero_mesa=%s, nombre_cliente=%s, ubicacion=%s, estado=%s, cantidad_personas=%s WHERE id_mesa=%s;"
				base_datos.execute(query, (
				nuevo_numero, nuevo_cliente, nueva_ubicacion, nuevo_estado_mesa, nueva_capacidad, id_mesa))
				conectar.commit()

				# Actualizar en la interfaz - usar el mismo formato con iconos
				estado_lower = nuevo_estado_mesa.lower() if nuevo_estado_mesa else "libre"
				if "libre" in estado_lower:
					mesa_color = COLORS['mesa_libre']
					estado_icon = "✅"
				elif "reservado" in estado_lower:
					mesa_color = COLORS['mesa_reservada']
					estado_icon = "🔴"
				else:
					mesa_color = COLORS['mesa_ocupada']
					estado_icon = "🟡"
				
				texto_actualizado = f"{ICONS['mesa']} Mesa {nuevo_numero}\n{ICONS['usuario']} {nuevo_cliente or 'Sin cliente'}\n{ICONS['ubicacion']} {nueva_ubicacion}\n{estado_icon} {nuevo_estado_mesa}\n{ICONS['personas']} {nueva_capacidad} personas"
				self.mesa_seleccionada.config(text=texto_actualizado, bg=mesa_color)
				self.ventana_modificar_mesa.destroy()
			else:
				messagebox.showerror("Error", "No se encontró el ID de la mesa en la base de datos.")
