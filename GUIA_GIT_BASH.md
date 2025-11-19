# Guía para Ejecutar el Programa en Git Bash

Esta guía te ayudará a ejecutar el Sistema de Gestión de Restaurante usando Git Bash en Windows.

## Requisitos Previos

1. **Python 3.7 o superior** instalado
2. **MySQL o MariaDB** instalado y corriendo
3. **Git Bash** instalado (viene con Git para Windows)

## Pasos para Ejecutar

### Opción 1: Usando el Script Automático (Recomendado)

1. **Abre Git Bash** en la carpeta del proyecto:
   ```bash
   # Navega a la carpeta del proyecto
   cd /d/Usuario/Desktop/Itec-Materias/Proyectos/Restaurante
   ```

2. **Da permisos de ejecución al script** (solo la primera vez):
   ```bash
   chmod +x ejecutar.sh
   ```

3. **Ejecuta el script**:
   ```bash
   ./ejecutar.sh
   ```

El script automáticamente:
- Verificará que Python esté instalado
- Instalará las dependencias si faltan
- Ejecutará el programa

### Opción 2: Ejecución Manual

1. **Abre Git Bash** y navega al proyecto:
   ```bash
   cd /d/Usuario/Desktop/Itec-Materias/Proyectos/Restaurante
   ```

2. **Verifica que Python esté instalado**:
   ```bash
   python --version
   # o
   python3 --version
   ```

3. **Instala las dependencias** (si no las tienes instaladas):
   ```bash
   pip install -r Proyecto-restaurante.python/requirements.txt
   # o
   python3 -m pip install -r Proyecto-restaurante.python/requirements.txt
   ```

4. **Navega al directorio del proyecto**:
   ```bash
   cd Proyecto-restaurante.python
   ```

5. **Ejecuta el programa**:
   ```bash
   python main.py
   # o
   python3 main.py
   ```

## Configuración de MySQL

Antes de ejecutar el programa, asegúrate de:

1. **MySQL está corriendo**:
   - En Windows, verifica en "Servicios" que MySQL esté iniciado
   - O ejecuta: `net start MySQL` (en PowerShell como administrador)

2. **La base de datos está creada**:
   ```bash
   mysql -u root -p < Proyecto-restaurante.python/schema.sql
   ```

3. **Las credenciales están correctas** en `Proyecto-restaurante.python/app/config.py`:
   - Por defecto usa: usuario `root`, contraseña `12345678`
   - Puedes cambiarlas editando el archivo o usando variables de entorno

## Variables de Entorno (Opcional)

Si quieres cambiar las credenciales sin editar el archivo, puedes usar variables de entorno en Git Bash:

```bash
export DB_USER="tu_usuario"
export DB_PASSWORD="tu_contraseña"
export DB_HOST="localhost"
export DB_NAME="reserva_restaurante"
```

Luego ejecuta el programa normalmente.

## Solución de Problemas

### Error: "python: command not found"
**Solución**: 
- Verifica que Python esté instalado: `python --version`
- Si usas `python3`, cambia el comando a `python3`
- Asegúrate de que Python esté en el PATH del sistema

### Error: "No module named 'mysql.connector'"
**Solución**: 
```bash
pip install -r Proyecto-restaurante.python/requirements.txt
```

### Error: "Can't connect to MySQL server"
**Solución**: 
1. Verifica que MySQL esté corriendo
2. Revisa las credenciales en `config.py`
3. Asegúrate de que la base de datos exista

### Error: "Permission denied" al ejecutar ejecutar.sh
**Solución**: 
```bash
chmod +x ejecutar.sh
```

### El programa no abre la ventana gráfica
**Solución**: 
- Asegúrate de tener una interfaz gráfica disponible (X11 en Git Bash puede requerir configuración adicional)
- En Windows, Git Bash debería funcionar normalmente con Tkinter

## Notas Importantes

- En Git Bash, las rutas usan barras `/` en lugar de `\`
- El directorio `D:\` se representa como `/d/` en Git Bash
- Si tienes problemas con rutas, usa rutas relativas en lugar de absolutas

## Comandos Rápidos

```bash
# Navegar al proyecto
cd /d/Usuario/Desktop/Itec-Materias/Proyectos/Restaurante

# Instalar dependencias
pip install -r Proyecto-restaurante.python/requirements.txt

# Ejecutar (desde la raíz)
python Proyecto-restaurante.python/main.py

# O ejecutar (desde el directorio del proyecto)
cd Proyecto-restaurante.python
python main.py
```

