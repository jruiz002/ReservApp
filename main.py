from usuario import Usuario, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE
import threading

def simulate_reservations(event_id, num_users, isolation_level):
    threads = []
    for user_id in range(1, num_users + 1):
        user = Usuario(user_id, event_id, isolation_level)
        threads.append(user)
        user.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Parámetros de la simulación
    evento_id = 1  # ID del evento "Concierto de Rock"
    num_users = 5  # Simulando 5 usuarios
    isolation_level = SERIALIZABLE  # Puedes cambiar a READ_COMMITTED o REPEATABLE_READ

    print(f"Iniciando simulación con {num_users} usuarios y nivel de aislamiento {isolation_level}")
    simulate_reservations(evento_id, num_users, isolation_level)
