import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# Conexión a la base de datos
try:
    conectar = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="reserva_restaurante"
    )
    base_datos = conectar.cursor()
    print("Conexión exitosa a la base de datos")
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
    exit(1)  # Salir si no hay conexión

class MesasClienteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Reservar Mesas - Cliente")
        master.geometry("800x600")  # Ajustar el tamaño según necesidad
        master.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\Icono cliente.ico")
        # Frame para las mesas con scroll
        self.canvas = tk.Canvas(master, bg="white")
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Cargar las mesas existentes desde la base de datos
        self.cargar_mesas_desde_bd()

    def cargar_mesas_desde_bd(self):
        """Carga todas las mesas almacenadas en la base de datos"""
        try:
            base_datos.execute("SELECT id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, cantidad_personas FROM mesas")
            mesas_bd = base_datos.fetchall()
            print(f"Mesas obtenidas: {mesas_bd}")  # Para depuración

            if not mesas_bd:
                tk.Label(self.scrollable_frame, text="No hay mesas disponibles.", font=("Arial", 14), bg="white").pack(pady=20)
                return

            for mesa_bd in mesas_bd:
                id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, capacidad = mesa_bd
                self.crear_mesa(id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, capacidad)

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo cargar las mesas. Error: {error}")

    def crear_mesa(self, id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, capacidad):
        """Crea un botón para cada mesa y ajusta su funcionalidad según el estado"""
        if estado.lower() == "libre":
            color = "lightgreen"
            comando = lambda: self.reservar_mesa(id_mesa)
        else:
            color = "lightcoral"
            comando = lambda: self.ver_detalles_mesa(id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, capacidad)

        mesa_button = tk.Button(
            self.scrollable_frame,
            text=f"Mesa {numero_mesa}\nUbicación: {ubicacion}\nCapacidad: {capacidad} personas\nEstado: {estado}",
            width=25,
            height=5,
            bg=color,
            command=comando
        )

        mesa_button.pack(padx=10, pady=10, side=tk.LEFT)

    def reservar_mesa(self, id_mesa):
        """Reserva la mesa seleccionada solicitando el nombre del cliente"""
        nombre_cliente = simpledialog.askstring("Reserva de Mesa", "Por favor, introduce tu nombre:")

        if nombre_cliente:
            try:
                # Actualizar el estado y el nombre del cliente en la base de datos
                query = "UPDATE mesas SET estado = 'Reservado', nombre_cliente = %s WHERE id_mesa = %s AND estado = 'Libre'"
                base_datos.execute(query, (nombre_cliente, id_mesa))
                conectar.commit()

                if base_datos.rowcount == 0:
                    messagebox.showwarning("Reserva Fallida", "La mesa ya ha sido reservada por otro cliente.")
                else:
                    messagebox.showinfo("Reserva Exitosa", "La mesa ha sido reservada con éxito.")
                    self.actualizar_interfaz()

            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo reservar la mesa. Error: {error}")
        else:
            messagebox.showinfo("Reserva Cancelada", "No se ha ingresado un nombre. La reserva ha sido cancelada.")

    def ver_detalles_mesa(self, id_mesa, numero_mesa, nombre_cliente, ubicacion, estado, capacidad):
        """Muestra los detalles de una mesa reservada"""
        detalles = f"**Detalles de la Mesa {numero_mesa}**\n\n" \
                   f"Ubicación: {ubicacion}\n" \
                   f"Capacidad: {capacidad} personas\n" \
                   f"Estado: {estado}\n" \
                   f"Nombre del Cliente: {nombre_cliente}"
        messagebox.showinfo("Detalles de la Mesa", detalles)

    def actualizar_interfaz(self):
        """Recarga las mesas para reflejar los cambios en la reserva"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.cargar_mesas_desde_bd()
