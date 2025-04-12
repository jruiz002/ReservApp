# Proyecto de Reserva de Asientos

Este proyecto simula la gestión de la reserva de asientos con concurrencia y manejo de niveles de aislamiento en una base de datos PostgreSQL.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)

## Requisitos

- Python 3.x
- PostgreSQL
- psycopg2

## Instalación

1. Clona el repositorio.
   ```bash
   git clone https://github.com/jruiz002/ReservApp.git
2. Instala las dependencias:
   ```bash
   pip install python-dotenv
   pip install psycopg2
   pip install psycopg2-binary
   ```

3. Configura las credenciales en el archivo .env
   ```bash
   cp .env.example .env
   ```

4. Crea la base de datos en PostgreSQL
   - Ejecuta el archivo ddl.sql
   - Ejecuta el archivo data.sql

## Uso
Ejecuta el archivo main.py para iniciar la simulación.
```bash
python main.py
```
