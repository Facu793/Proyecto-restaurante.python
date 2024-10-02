import tkinter as tk
from ventana_administrador import MesasGUI
from ventana_cliente import MesasClienteGUI

class LoginGUI:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\pizza_0vQ_icon.ico")
        master.configure(bg="light green")

        # Crear los widgets
        self.lbl_nombre = tk.Label(master, text="Nombre de usuario:")
        self.lbl_contrasenia = tk.Label(master, text="Contraseña:")
        self.entry_nombre = tk.Entry(master)
        self.entry_contrasenia = tk.Entry(master, show="*")
        self.btn_inicio_sesion = tk.Button(master, text="Iniciar sesión", command=self.login)
        self.btn_registro = tk.Button(master, text="Registrarse", command=self.open_register_window)

        # Organizar los widgets en la ventana
        self.lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        self.lbl_contrasenia.grid(row=1, column=0, padx=10, pady=10)
        self.entry_contrasenia.grid(row=1, column=1, padx=10, pady=10)
        self.btn_inicio_sesion.grid(row=2, column=0, padx=10, pady=10)
        self.btn_registro.grid(row=2, column=1, padx=10, pady=10)

    def open_register_window(self):
        self.registro_window = tk.Toplevel(self.master)
        self.registro_window.title("Registro de usuario")
        self.registro_window.iconbitmap("D:\\Usuario\\Desktop\\Itec-Materias\\2do año Itec-2024\\Itec-Programacion I\\T.P Anual Pogramacion 1\\agregar_usuario.ico")

        # Crear los widgets para la ventana de registro
        self.lbl_primer_nombre = tk.Label(self.registro_window, text="Nombre de usuario:")
        self.lbl_apellido = tk.Label(self.registro_window, text="Apellido:")
        self.lbl_sexo = tk.Label(self.registro_window, text="Sexo:")
        self.lbl_rol = tk.Label(self.registro_window, text="Rol (Admin o Cliente):")
        self.lbl_contrasenia = tk.Label(self.registro_window, text="Contraseña:")
        self.entry_primer_nombre = tk.Entry(self.registro_window)
        self.entry_apellido = tk.Entry(self.registro_window)
        self.var_sexo = tk.StringVar()
        self.var_rol = tk.StringVar()
        self.rb_masculino = tk.Radiobutton(self.registro_window, text="Masculino", variable=self.var_sexo, value="Masculino")
        self.rb_femenino = tk.Radiobutton(self.registro_window, text="Femenino", variable=self.var_sexo, value="Femenino")
        self.entry_contrasenia = tk.Entry(self.registro_window, show="*")
        self.entry_rol = tk.Entry(self.registro_window)  # Para introducir el rol
        self.btn_register = tk.Button(self.registro_window, text="Registrarse", command=self.register_user)

        # Organizar los widgets en la ventana de registro
        self.lbl_primer_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.entry_primer_nombre.grid(row=0, column=1, padx=10, pady=10)
        self.lbl_apellido.grid(row=1, column=0, padx=10, pady=10)
        self.entry_apellido.grid(row=1, column=1, padx=10, pady=10)
        self.lbl_sexo.grid(row=2, column=0, padx=10, pady=10)
        self.rb_masculino.grid(row=2, column=1, padx=10, pady=10)
        self.rb_femenino.grid(row=2, column=2, padx=10, pady=10)
        self.lbl_rol.grid(row=3, column=0, padx=10, pady=10)
        self.entry_rol.grid(row=3, column=1, padx=10, pady=10)  # Para introducir el rol
        self.lbl_contrasenia.grid(row=4, column=0, padx=10, pady=10)
        self.entry_contrasenia.grid(row=4, column=1, padx=10, pady=10)
        self.btn_register.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def register_user(self):
        # Obtener los valores de los campos de registro
        primer_nombre = self.entry_primer_nombre.get()
        apellido = self.entry_apellido.get()
        sexo = self.var_sexo.get()
        contrasenia = self.entry_contrasenia.get()
        rol = self.entry_rol.get()  # Nuevo campo para el rol

        # Guardar los datos en un archivo de texto
        with open("D:\\Usuario\\Desktop\\Pychar-VirtualEnvt.p.programación\\Prueba-registro.tx", "a") as file:
            file.write(f"Nombre: {primer_nombre}\n")
            file.write(f"Apellido: {apellido}\n")
            file.write(f"Sexo: {sexo}\n")
            file.write(f"Rol: {rol}\n")  # Guardar el rol del usuario
            file.write(f"Contraseña: {contrasenia}\n")
            file.write("-------------------\n")

        print(f"Nombre: {primer_nombre}")
        print(f"Apellido: {apellido}")
        print(f"Sexo: {sexo}")
        print(f"Rol: {rol}")
        print(f"Contraseña: {contrasenia}")

    def login(self):
        # Obtener los valores de los campos de entrada en la ventana de inicio de sesión
        nombre = self.entry_nombre.get()
        contrasenia = self.entry_contrasenia.get()
        usuario_valido = False  # Variable para verificar si el usuario es válido

        # Validar los datos del usuario en el archivo de texto
        with open("D:\\Usuario\\Desktop\\Pychar-VirtualEnvt.p.programación\\Prueba-registro.tx", "r") as txt:
            archivo = txt.readlines()

            # Iterar sobre las líneas del archivo
            for i in range(len(archivo)):
                if archivo[i].startswith("Nombre:"):
                    nombre_registrado = archivo[i].split(": ")[1].strip()
                    if nombre == nombre_registrado:
                        contrasenia_registrada = archivo[i + 4].split(": ")[1].strip()
                        if contrasenia == contrasenia_registrada:
                            rol = archivo[i + 3].split(": ")[1].strip()
                            usuario_valido = True
                            print("Inicio de sesión exitoso")
                            if rol == "Admin":
                                ventana_administrador_acceso=tk.Toplevel(root)
                                MesasGUI(ventana_administrador_acceso)

                            else:
                                ventana_cliente_acceso=tk.Toplevel(root)
                                MesasClienteGUI(ventana_cliente_acceso)
                            break

            if not usuario_valido:
                print("Nombre de usuario o contraseña inválidos")






# Iniciar la aplicación
root = tk.Tk()
login_gui = LoginGUI(root)
root.mainloop()
