#!/bin/bash

# Script para ejecutar el programa del Restaurante en Git Bash
# Uso: ./ejecutar.sh

echo "=========================================="
echo "  Sistema de Gestión de Restaurante"
echo "=========================================="
echo ""

# Verificar si Python está instalado
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python no está instalado o no está en el PATH"
    echo "   Por favor, instala Python 3.7 o superior desde https://www.python.org/downloads/"
    exit 1
fi

# Determinar el comando de Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python"
fi

echo "✓ Python encontrado: $($PYTHON_CMD --version)"
echo ""

# Verificar si las dependencias están instaladas
echo "Verificando dependencias..."
if ! $PYTHON_CMD -c "import mysql.connector" 2>/dev/null; then
    echo "⚠ Advertencia: mysql-connector-python no está instalado"
    echo "   Instalando dependencias..."
    $PYTHON_CMD -m pip install -r Proyecto-restaurante.python/requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✓ Dependencias verificadas"
fi
echo ""

# Verificar si MySQL está configurado
echo "Verificando configuración de MySQL..."
if ! $PYTHON_CMD -c "from app.config import DB_CONFIG; print('Configuración cargada')" 2>/dev/null; then
    echo "⚠ Advertencia: No se pudo cargar la configuración"
fi
echo ""

# Cambiar al directorio del proyecto
cd Proyecto-restaurante.python 2>/dev/null || {
    echo "❌ Error: No se encontró el directorio Proyecto-restaurante.python"
    exit 1
}

# Ejecutar el programa
echo "=========================================="
echo "  Iniciando aplicación..."
echo "=========================================="
echo ""
$PYTHON_CMD main.py

