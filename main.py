import threading
import random
import time
from db.conexion import connect_db
from db.funciones_reservas import reserve_seat
from db.funciones_usuarios import get_first_n_users
from db.setup_data import setup_simulacion 

def simulate_reservations(num_users, isolation_level, num_seats):
    conn = connect_db()
    if not conn:
        return

    setup_simulacion(conn, num_seats)

    user_ids = get_first_n_users(conn, num_users)
    assigned_seats = [random.randint(1, num_seats) for _ in range(num_users)]

    reservas_exitosas = []  # [(usuario_id, asiento, duracion)]
    reservas_fallidas = []  # [(usuario_id, asiento)]
    total_duracion = 0

    def reserve_for_user(user_id, seat_id):
        nonlocal total_duracion
        hilo_conn = connect_db()
        start_time = time.time()
        success = reserve_seat(hilo_conn, user_id, seat_id, isolation_level)
        duration = time.time() - start_time
        hilo_conn.close()

        if success:
            reservas_exitosas.append((user_id, seat_id, duration))
        else:
            reservas_fallidas.append((user_id, seat_id))
        total_duracion += duration

    threads = []
    for user_id, seat_id in zip(user_ids, assigned_seats):
        t = threading.Thread(target=reserve_for_user, args=(user_id, seat_id))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Encabezado con resumen
    print("\n=== RESUMEN DE LA SIMULACIÓN ===")
    print(f"Nivel de aislamiento: {isolation_level}")
    print(f"Usuarios simulados: {num_users}")
    print(f"Asientos disponibles: {num_seats}")
    print(f"Reservas exitosas: {len(reservas_exitosas)}")
    print(f"Reservas fallidas: {len(reservas_fallidas)}")
    print(f"Tiempo total de transacciones: {total_duracion:.4f} segundos")

    # Detalle de exitosas
    print("\n Detalle de reservas exitosas:")
    for user_id, seat_id, duracion in reservas_exitosas:
        print(f"Usuario {user_id} reservó el asiento {seat_id} | Tiempo: {duracion:.4f}s")

    # Detalle de fallidas
    print("\n Detalle de reservas fallidas:")
    for user_id, seat_id in reservas_fallidas:
        print(f"Usuario {user_id} no pudo reservar el asiento {seat_id}")

    conn.close()

def start_simulation():
    while True:
        print("\n=== ReservApp - Simulación de Reservas ===")
        print("Seleccione el nivel de aislamiento:")
        print("1. READ COMMITTED")
        print("2. REPEATABLE READ")
        print("3. SERIALIZABLE")
        print("0. Salir")

        try:
            level_choice = int(input("\nIngrese su elección: "))
            if level_choice == 0:
                print("Saliendo de la simulación.")
                break
            elif 1 <= level_choice <= 3:
                isolation_levels = {
                    1: "READ COMMITTED",
                    2: "REPEATABLE READ",
                    3: "SERIALIZABLE"
                }
                isolation_level = isolation_levels[level_choice]
            else:
                print("Por favor, ingrese un número entre 0 y 3.")
                continue
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        while True:
            try:
                num_users = int(input("\nIngrese el número de usuarios para la simulación: "))
                if num_users > 0 and num_users <= 30:
                    break
                print("El número de usuarios debe ser mayor que 0 y menor o igual a 30.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

        num_seats = num_users

        print("\n----------------------------------------------------")
        simulate_reservations(num_users, isolation_level, num_seats)


if __name__ == "__main__":
    start_simulation()
