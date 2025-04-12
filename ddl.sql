--Fase 1: Diseño de la Base de Datos
BEGIN;

-- Creación de la tabla Usuarios
CREATE TABLE Usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Creación de la tabla Asientos
CREATE TABLE Asientos (
    id_asiento SERIAL PRIMARY KEY,
	estado BOOLEAN NOT NULL
);

-- Creación de la tabla Reservas
CREATE TABLE Reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_asiento INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_asiento) REFERENCES Asientos(id_asiento) ON DELETE CASCADE
);

COMMIT;
