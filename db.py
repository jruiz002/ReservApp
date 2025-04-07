import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )
        return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# Iniciar una transacción con un nivel de aislamiento específico
def start_transaction(connection, isolation_level):
    connection.set_isolation_level(isolation_level)

# Ejecutar una consulta en la base de datos
def execute_query(connection, query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()

# Obtener los asientos disponibles para un evento
def get_available_seats(connection, event_id):
    query = sql.SQL("SELECT * FROM Asientos WHERE id_evento = %s AND id_asiento NOT IN (SELECT id_asiento FROM Reservas WHERE estado = TRUE)")
    with connection.cursor() as cursor:
        cursor.execute(query, (event_id,))
        return cursor.fetchall()
