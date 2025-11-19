-- Esquema de base de datos para el sistema de gestión de restaurante
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS reserva_restaurante;
USE reserva_restaurante;

-- Tabla de mesas
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

-- Tabla de usuarios
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

-- Índices para mejorar el rendimiento
CREATE INDEX idx_estado ON mesas(estado);
CREATE INDEX idx_numero_mesa ON mesas(numero_mesa);
CREATE INDEX idx_nombre_usuario ON usuarios(nombre_usuario);
CREATE INDEX idx_rol ON usuarios(rol);

