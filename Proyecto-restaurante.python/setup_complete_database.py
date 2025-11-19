"""
Script completo para crear la base de datos y todas las tablas necesarias
Ejecuta este script una vez para configurar toda la base de datos
"""
import mysql.connector
from app.config import DB_CONFIG

def crear_base_datos():
    """Crea la base de datos si no existe"""
    try:
        # Conectar sin especificar la base de datos
        config_sin_db = DB_CONFIG.copy()
        config_sin_db.pop('database', None)
        
        conexion = mysql.connector.connect(**config_sin_db)
        cursor = conexion.cursor()
        
        print("Creando base de datos 'reserva_restaurante'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS reserva_restaurante")
        print("[OK] Base de datos creada o ya existe")
        
        cursor.close()
        conexion.close()
        
    except mysql.connector.Error as err:
        print(f"[ERROR] Error al crear la base de datos: {err}")
        return False
    return True

def crear_tabla_mesas():
    """Crea la tabla de mesas en la base de datos"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()

        print("Creando tabla de mesas...")

        query = """
        CREATE TABLE IF NOT EXISTS mesas (
            id_mesa INT AUTO_INCREMENT PRIMARY KEY,
            numero_mesa VARCHAR(10) NOT NULL UNIQUE,
            nombre_cliente VARCHAR(100) DEFAULT NULL,
            ubicacion VARCHAR(50) NOT NULL,
            estado VARCHAR(20) NOT NULL DEFAULT 'Libre',
            cantidad_personas INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)

        # Crear índices
        print("Creando indices para mesas...")
        try:
            cursor.execute("CREATE INDEX idx_estado ON mesas(estado);")
        except mysql.connector.Error:
            pass  # El indice ya existe

        try:
            cursor.execute("CREATE INDEX idx_numero_mesa ON mesas(numero_mesa);")
        except mysql.connector.Error:
            pass  # El indice ya existe

        conexion.commit()
        print("[OK] Tabla de mesas creada exitosamente!")

        cursor.close()
        conexion.close()
        return True

    except mysql.connector.Error as err:
        print(f"[ERROR] Error al crear la tabla de mesas: {err}")
        return False

def crear_tabla_usuarios():
    """Crea la tabla de usuarios en la base de datos"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()

        print("Creando tabla de usuarios...")

        query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
            apellido VARCHAR(50) NOT NULL,
            sexo VARCHAR(10) NOT NULL,
            rol VARCHAR(20) NOT NULL,
            contraseña VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)

        # Crear índices
        print("Creando indices para usuarios...")
        try:
            cursor.execute("CREATE INDEX idx_nombre_usuario ON usuarios(nombre_usuario);")
        except mysql.connector.Error:
            pass  # El indice ya existe

        try:
            cursor.execute("CREATE INDEX idx_rol ON usuarios(rol);")
        except mysql.connector.Error:
            pass  # El indice ya existe

        conexion.commit()
        print("[OK] Tabla de usuarios creada exitosamente!")

        # Verificar que la tabla existe
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        if cursor.fetchone():
            print("[OK] Verificacion: La tabla 'usuarios' existe en la base de datos.")
        
        cursor.close()
        conexion.close()
        return True

    except mysql.connector.Error as err:
        print(f"[ERROR] Error al crear la tabla de usuarios: {err}")
        return False

def verificar_tablas():
    """Verifica que todas las tablas necesarias existen"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        tablas_nombres = [tabla[0] for tabla in tablas]
        
        print("\n--- Tablas en la base de datos ---")
        for tabla in tablas_nombres:
            print(f"  - {tabla}")
        
        if 'mesas' in tablas_nombres and 'usuarios' in tablas_nombres:
            print("\n[OK] Todas las tablas necesarias estan creadas!")
            return True
        else:
            print("\n[ADVERTENCIA] Faltan algunas tablas")
            return False
        
        cursor.close()
        conexion.close()
        
    except mysql.connector.Error as err:
        print(f"[ERROR] Error al verificar tablas: {err}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Configuracion Completa de Base de Datos")
    print("=" * 60)
    print()
    
    # Crear base de datos
    if crear_base_datos():
        print()
        
        # Crear tabla de mesas
        if crear_tabla_mesas():
            print()
            
            # Crear tabla de usuarios
            if crear_tabla_usuarios():
                print()
                
                # Verificar todas las tablas
                verificar_tablas()
                print()
                print("=" * 60)
                print("[OK] Configuracion completada exitosamente!")
                print("=" * 60)
            else:
                print("\n[ERROR] No se pudo crear la tabla de usuarios")
        else:
            print("\n[ERROR] No se pudo crear la tabla de mesas")
    else:
        print("\n[ERROR] No se pudo crear la base de datos")

