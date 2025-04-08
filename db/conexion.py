import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
def connect_db():
    """Función para conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
