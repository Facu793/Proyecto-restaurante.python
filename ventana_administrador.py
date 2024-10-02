import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
conectar = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="reserva_restaurante"
)

base_datos = conectar.cursor()


class MesasGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mesas Disponibles")
        master.geometry("800x940")
        master.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\Icono administrador.ico")

        # Frame para las mesas
        self.frame_mesas = tk.Frame(master, bg="lightgrey")
        self.frame_mesas.place(relwidth=1, relheight=0.8)

        # Botones para añadir, eliminar y modificar mesa
        self.btn_add_mesa = tk.Button(master, text="Añadir Mesa", command=self.abrir_ventana_anadir_mesa)
        self.btn_add_mesa.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_delete_mesa = tk.Button(master, text="Eliminar Mesa Seleccionada",
                                         command=self.eliminar_mesa_seleccionada)
        self.btn_delete_mesa.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_modificar_mesa = tk.Button(master, text="Modificar Mesa Seleccionada",
                                            command=self.abrir_ventana_modificar_mesa)
        self.btn_modificar_mesa.pack(side=tk.LEFT, padx=10, pady=10)

        # Lista para almacenar las mesas
        self.mesas = []
        self.mesa_seleccionada = None

        # Variables para mover mesas
        self.offset_x = 0
        self.offset_y = 0

        # Cargar las mesas existentes desde la base de datos
        self.cargar_mesas_desde_bd()

    def cargar_mesas_desde_bd(self):
        """Carga las mesas almacenadas en la base de datos al inicio"""
        base_datos.execute("SELECT numero_mesa,nombre_cliente, ubicacion, estado, cantidad_personas FROM mesas")
        mesas_bd = base_datos.fetchall()


        for mesa_bd in mesas_bd:

            numero_mesa,nombre_cliente, ubicacion,estado_mesa, cantidad_personas = mesa_bd
            self.crear_mesa(numero_mesa,nombre_cliente, ubicacion,estado_mesa,cantidad_personas)


    def crear_mesa(self, numero_mesa,nombre_cliente,ubicacion_mesa,estado_mesa,capacidad):### Estoy acomodando por que la base de dato no tiene la misma cantidad de campos que el codigo je
        """Crea una nueva mesa como botón y la coloca en el frame"""
        mesa_button = tk.Button(self.frame_mesas, text=f"Mesa {numero_mesa}\n Nombre cliente {nombre_cliente}\n Ubicación {ubicacion_mesa}\n Estado de la mesa: {estado_mesa}\n Capacidad: {capacidad}", width=20, height=5,
                                bg="lightblue")

        # Posicionar las mesas inicialmente
        x = (len(self.mesas) % 4) * 120 + 20
        y = (len(self.mesas) // 4) * 100 + 20
        mesa_button.place(x=x, y=y)

        # Bind de eventos para mover y seleccionar la mesa
        mesa_button.bind("<Button-1>", self.iniciar_mover_mesa)
        mesa_button.bind("<B1-Motion>", self.mover_mesa)
        mesa_button.bind("<ButtonRelease-1>", self.finalizar_mover_mesa)
        mesa_button.bind("<Button-3>", self.seleccionar_mesa)

        # Añadir el botón a la lista de mesas
        self.mesas.append(mesa_button)

    def iniciar_mover_mesa(self, event):
        """Inicia el movimiento de la mesa seleccionada"""
        self.mesa_seleccionada = event.widget
        self.offset_x = event.x
        self.offset_y = event.y

    def mover_mesa(self, event):
        """Mueve la mesa seleccionada dentro del frame"""
        if self.mesa_seleccionada:
            x = event.x_root - self.frame_mesas.winfo_rootx() - self.offset_x
            y = event.y_root - self.frame_mesas.winfo_rooty() - self.offset_y
            self.mesa_seleccionada.place(x=x, y=y)

    def finalizar_mover_mesa(self, event):
        """Finaliza el movimiento de la mesa"""
        self.mesa_seleccionada = None

    def seleccionar_mesa(self, event):
        """Selecciona la mesa cuando se hace click derecho sobre ella"""
        if self.mesa_seleccionada:
            self.mesa_seleccionada.config(bg="lightblue")

        self.mesa_seleccionada = event.widget
        self.mesa_seleccionada.config(bg="yellow")

    def abrir_ventana_anadir_mesa(self):
        """Abre una ventana emergente para añadir una nueva mesa con su número y capacidad"""
        self.ventana_anadir_mesa = tk.Toplevel(self.master)
        self.ventana_anadir_mesa.title("Añadir Mesa")
        self.ventana_anadir_mesa.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\mesa añadir mesa-icon.ico")

        tk.Label(self.ventana_anadir_mesa, text="Número de mesa:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_numero_mesa = tk.Entry(self.ventana_anadir_mesa)
        self.entry_numero_mesa.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.ventana_anadir_mesa, text="Nombre de cliente:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_nombre_cliente = tk.Entry(self.ventana_anadir_mesa)
        self.entry_nombre_cliente.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.ventana_anadir_mesa, text="Ubicación:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_ubicacion = tk.Entry(self.ventana_anadir_mesa)
        self.entry_ubicacion.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.ventana_anadir_mesa, text="Estado:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_estado = tk.Entry(self.ventana_anadir_mesa)
        self.entry_estado.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.ventana_anadir_mesa, text="Cantidad de personas:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_capacidad_mesa = tk.Entry(self.ventana_anadir_mesa)
        self.entry_capacidad_mesa.grid(row=4, column=1, padx=10, pady=10)


        btn_confirmar = tk.Button(self.ventana_anadir_mesa, text="Añadir", command=self.anadir_mesa)
        btn_confirmar.grid(row=5, columnspan=2, pady=10)

    def anadir_mesa(self):
        """Añade una nueva mesa con número personalizado y capacidad desde la ventana emergente"""
        numero_mesa = self.entry_numero_mesa.get()
        nombre_cliente=self.entry_nombre_cliente.get()
        ubicacion_mesa=self.entry_ubicacion.get()
        estado_mesa=self.entry_estado.get()
        capacidad_mesa = self.entry_capacidad_mesa.get()




        if numero_mesa and numero_mesa.isdigit() and nombre_cliente and ubicacion_mesa  and capacidad_mesa and capacidad_mesa.isdigit():
            for mesa in self.mesas:
                if mesa.cget("text").startswith(f"Mesa {numero_mesa}"):
                    messagebox.showerror("Error", f"Ya existe una mesa con el número {numero_mesa}.")
                    return
            self.crear_mesa(numero_mesa,nombre_cliente,ubicacion_mesa,estado_mesa,capacidad_mesa)

            # Insertar en la base de datos
            query = "INSERT INTO mesas (numero_mesa, nombre_cliente, ubicacion, estado, cantidad_personas) VALUES (%s, %s, %s, %s, %s);"
            valores = (numero_mesa, nombre_cliente, ubicacion_mesa,estado_mesa, capacidad_mesa)
            base_datos.execute(query, valores)
            conectar.commit()

            self.ventana_anadir_mesa.destroy()
        else:
            messagebox.showwarning("Entrada no válida",
                                   "Por favor, introduce valores numéricos válidos para el número de mesa y capacidad.")

    def eliminar_mesa_seleccionada(self):
        """Elimina la mesa seleccionada"""
        if self.mesa_seleccionada:
            respuesta = messagebox.askyesno("Eliminar Mesa",
                                            f"¿Estás seguro de eliminar {self.mesa_seleccionada.cget('text')}?")
            if respuesta:
                # Obtener el ID de la mesa a eliminar
                numero_mesa = self.mesa_seleccionada.cget("text").split("\n")[0].replace("Mesa ", "")

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
            messagebox.showwarning("Sin selección", "No has seleccionado ninguna mesa para modificar.")
            return

        self.ventana_modificar_mesa = tk.Toplevel(self.master)
        self.ventana_modificar_mesa.title("Modificar Mesa")
        self.ventana_modificar_mesa.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\modificar mesa.ico")

        # Ver el texto de la mesa seleccionada para depuración
        texto_mesa = self.mesa_seleccionada.cget("text")
        print(f"Texto de la mesa seleccionada: {texto_mesa}")  # Para depurar

        # Ahora el texto tiene 4 líneas: número, cliente, ubicación, estado, capacidad
        try:
            numero_actual, cliente_actual, ubicacion_actual,estado_actual, capacidad_actual = texto_mesa.split("\n")
            numero_actual = numero_actual.replace("Mesa ", "").strip()  # Obtener el número de mesa
            cliente_actual = cliente_actual.replace("Cliente: ", "").strip()  # Obtener el cliente
            ubicacion_actual = ubicacion_actual.replace("Ubicación: ", "").strip()  # Obtener la ubicación
            estado_actual= estado_actual.replace("Estado: ","").strip() #Obtener el estado de la mesa
            capacidad_actual = capacidad_actual.replace("Capacidad: ", "").strip()  # Obtener la capacidad
        except ValueError:
            messagebox.showerror("Error", "El formato del texto de la mesa seleccionada no es el esperado.")
            return

        # Crear campos de entrada para los valores actuales
        tk.Label(self.ventana_modificar_mesa, text="Número de mesa:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_modificar_numero = tk.Entry(self.ventana_modificar_mesa)
        self.entry_modificar_numero.grid(row=0, column=1, padx=10, pady=10)
        self.entry_modificar_numero.insert(0, numero_actual)

        tk.Label(self.ventana_modificar_mesa, text="Nombre cliente:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_modificar_cliente = tk.Entry(self.ventana_modificar_mesa)
        self.entry_modificar_cliente.grid(row=1, column=1, padx=10, pady=10)
        self.entry_modificar_cliente.insert(0, cliente_actual)

        tk.Label(self.ventana_modificar_mesa, text="Ubicación:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_modificar_ubicacion = tk.Entry(self.ventana_modificar_mesa)
        self.entry_modificar_ubicacion.grid(row=2, column=1, padx=10, pady=10)
        self.entry_modificar_ubicacion.insert(0, ubicacion_actual)

        tk.Label(self.ventana_modificar_mesa, text="Estado de la mesa:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_modificar_estado = tk.Entry(self.ventana_modificar_mesa)
        self.entry_modificar_estado.grid(row=3, column=1, padx=10, pady=10)
        self.entry_modificar_estado.insert(0, estado_actual)

        tk.Label(self.ventana_modificar_mesa, text="Capacidad de la mesa:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_modificar_capacidad = tk.Entry(self.ventana_modificar_mesa)
        self.entry_modificar_capacidad.grid(row=4, column=1, padx=10, pady=10)
        self.entry_modificar_capacidad.insert(0, capacidad_actual)

        btn_confirmar = tk.Button(self.ventana_modificar_mesa, text="Guardar Cambios", command=self.modificar_mesa)
        btn_confirmar.grid(row=5, columnspan=2, pady=10)

    def modificar_mesa(self):
        """Modifica el número, cliente, ubicación, estado y la capacidad de la mesa seleccionada"""
        nuevo_numero = self.entry_modificar_numero.get()
        nuevo_cliente = self.entry_modificar_cliente.get()
        nueva_ubicacion = self.entry_modificar_ubicacion.get()
        nuevo_estado_mesa=self.entry_modificar_estado.get()
        nueva_capacidad = self.entry_modificar_capacidad.get()

        if nuevo_numero and nuevo_numero.isdigit() and nueva_capacidad and nueva_capacidad.isdigit():
            # Verificar que no haya otra mesa con el mismo número
            for mesa in self.mesas:
                if mesa != self.mesa_seleccionada and mesa.cget("text").startswith(f"Mesa {nuevo_numero}"):
                    messagebox.showerror("Error", f"Ya existe una mesa con el número {nuevo_numero}.")
                    return

            # Actualizar en la base de datos
            numero_actual = self.mesa_seleccionada.cget("text").split("\n")[0].replace("Mesa ", "")
            query = "UPDATE mesas SET nombre_cliente=%s, ubicacion=%s, estado=%s, cantidad_personas=%s WHERE id_mesa=%s;"
            base_datos.execute(query, (nuevo_cliente, nueva_ubicacion,nuevo_estado_mesa, nueva_capacidad,numero_actual))
            conectar.commit()

            # Actualizar en la interfaz
            self.mesa_seleccionada.config(
                text=f"Mesa {nuevo_numero}\nNombre de cliente: {nuevo_cliente}\nUbicación: {nueva_ubicacion}\n Estado de la mesa: {nuevo_estado_mesa}\nCapacidad: {nueva_capacidad}"
            )
            self.ventana_modificar_mesa.destroy()

# Iniciar la aplicación
root = tk.Tk()
login_gui = MesasGUI(root)
root.mainloop()
