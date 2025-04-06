import threading
from db import connect_db, start_transaction, execute_query, get_available_seats
import random
import time

# Definir los niveles de aislamiento
READ_COMMITTED = 2
REPEATABLE_READ = 4
SERIALIZABLE = 8

class Usuario(threading.Thread):
    def __init__(self, id_usuario, evento_id, isolation_level, num_intentos=1):
        threading.Thread.__init__(self)
        self.id_usuario = id_usuario
        self.evento_id = evento_id
        self.isolation_level = isolation_level
        self.num_intentos = num_intentos
        self.connection = connect_db()
        start_transaction(self.connection, self.isolation_level)

    def run(self):
        for _ in range(self.num_intentos):
            try:
                available_seats = get_available_seats(self.connection, self.evento_id)
                if available_seats:
                    # Elegir un asiento aleatorio
                    seat_id = random.choice(available_seats)[0]
                    print(f"Usuario {self.id_usuario} intenta reservar el asiento {seat_id}")
                    # Reservar el asiento
                    query = "INSERT INTO Reservas (id_usuario, id_evento, id_asiento, estado) VALUES (%s, %s, %s, TRUE)"
                    execute_query(self.connection, query, (self.id_usuario, self.evento_id, seat_id))
                    print(f"Usuario {self.id_usuario} reservó el asiento {seat_id} con éxito!")
                else:
                    print(f"Usuario {self.id_usuario} no encontró asientos disponibles.")
                time.sleep(random.uniform(0.1, 0.5))  # Simula el retraso de cada intento
            except Exception as e:
                print(f"Error al intentar reservar: {e}")

    def close_connection(self):
        self.connection.close()
