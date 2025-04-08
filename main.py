import threading
from db.conexion import connect_db
from db.funciones_reservas import reserve_seat
import random
import time

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
        start_time = time.time()
        success = reserve_seat(conn, user_id, seat_id, isolation_level)
        duration = time.time() - start_time
        if success:
            print(f"Usuario {user_id} asignado al asiento {seat_id} | Tiempo de transacción: {duration:.4f}s")
        else:
            print(f"Error: Usuario {user_id} no pudo reservar el asiento {seat_id}")
    
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

def start_simulation():
    print("\n=== ReservApp - Simulación de Reservas ===")
    print("Seleccione el nivel de aislamiento:")
    print("1. READ COMMITTED")
    print("2. REPEATABLE READ")
    print("3. SERIALIZABLE")
    
    while True:
        try:
            level_choice = int(input("\nIngrese su elección: "))
            if 1 <= level_choice <= 3:
                break
            print("Por favor, ingrese un número entre 1 y 3.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    isolation_levels = {
        1: "READ COMMITTED",
        2: "REPEATABLE READ",
        3: "SERIALIZABLE"
    }
    isolation_level = isolation_levels[level_choice]
    
    while True:
        try:
            num_users = int(input("\nIngrese el número de usuarios para la simulación: "))
            if num_users > 0:
                break
            print("El número de usuarios debe ser mayor que 0.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    num_seats = 100  # Suponiendo que hay 100 asientos disponibles
    
    print(f"\nIniciando simulación con {num_users} usuarios y nivel de aislamiento {isolation_level}...")
    simulate_reservations(num_users, isolation_level, num_seats)

if __name__ == "__main__":
    start_simulation()
