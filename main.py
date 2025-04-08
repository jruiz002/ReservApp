import threading
from db.conexion import connect_db
from db.funciones_reservas import reserve_seat
import random

def assign_seats(num_users, num_seats):
    """Asigna aleatoriamente un asiento a cada usuario."""
    return random.sample(range(1, num_seats + 1), num_users)

def simulate_reservations(num_users, isolation_level, num_seats):
    conn = connect_db()
    if not conn:
        return

    # Asignar asientos aleatorios a los usuarios
    assigned_seats = assign_seats(num_users, num_seats)
    
    # Función interna para reservar un asiento para un usuario
    def reserve_for_user(user_id, seat_id):
        reserve_seat(conn, user_id, seat_id, isolation_level)
    
    # Crear hilos para simular la concurrencia
    threads = []
    for user_id, seat_id in enumerate(assigned_seats, start=1):
        t = threading.Thread(target=reserve_for_user, args=(user_id, seat_id))
        threads.append(t)
        t.start()

    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()

    conn.close()

if __name__ == "__main__":
    num_users = int(input("¿Cuántos usuarios harán la reserva? "))
    isolation_level = input("Selecciona el nivel de aislamiento (READ COMMITTED, REPEATABLE READ, SERIALIZABLE): ")
    num_seats = 100  # Suponiendo que hay 100 asientos disponibles
    
    simulate_reservations(num_users, isolation_level, num_seats)
