# 🍽️ Sistema de Gestión de Restaurante

Sistema de gestión de mesas para restaurante con interfaz gráfica.

## 🛠️ Tecnologías
- **Python 3.7+** - Lenguaje de programación
- **Tkinter** - Interfaz gráfica de usuario (GUI)
- **MySQL** - Base de datos relacional
- **mysql-connector-python** - Conector para MySQL
- **Pillow** - Procesamiento de imágenes

## 🧰 Herramientas de Desarrollo
- **Git** - Control de versiones
- **GitHub** - Repositorio remoto
- **MySQL Workbench** - Gestión de base de datos (opcional)
- **PyCharm / VS Code** - Entorno de desarrollo (opcional)

## 📦 Instalación
```bash
# Instalar dependencias
pip install -r Proyecto-restaurante.python/requirements.txt

# Configurar base de datos
cd Proyecto-restaurante.python
python setup_complete_database.py
```

## 🚀 Ejecución
```bash
cd Proyecto-restaurante.python
python main.py
```

## 📝 Configuración
Edita `Proyecto-restaurante.python/app/config.py` con tus credenciales de MySQL:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña',
    'database': 'reserva_restaurante'
}
```

## ✨ Funcionalidades
- **Administrador**: Gestión completa de mesas (crear, modificar, eliminar)
- **Cliente**: Visualización y reserva de mesas disponibles
