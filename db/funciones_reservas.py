import psycopg2

def reserve_seat(conn, user_id, seat_id, isolation_level):
    cur = conn.cursor()

    # Establecer el nivel de aislamiento
    if isolation_level == "READ COMMITTED":
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    elif isolation_level == "REPEATABLE READ":
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ)
    elif isolation_level == "SERIALIZABLE":
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    else:
        raise ValueError("Nivel de aislamiento no reconocido")

    try:
        cur.execute("BEGIN;")
        
        # Verificar disponibilidad del asiento con FOR UPDATE para bloqueo
        cur.execute("SELECT estado FROM Asientos WHERE id_asiento = %s FOR UPDATE;", (seat_id,))
        seat = cur.fetchone()

        if seat and seat[0] == True:
            # Ya está reservado
            print(f"Usuario {user_id} no pudo reservar el asiento {seat_id}, ya está ocupado.")
            cur.execute("ROLLBACK;")
            return False
        else:
            # Disponible, proceder
            cur.execute("""
                INSERT INTO Reservas (id_usuario, id_asiento) 
                VALUES (%s, %s);
            """, (user_id, seat_id))
            cur.execute("UPDATE Asientos SET estado = TRUE WHERE id_asiento = %s;", (seat_id,))
            cur.execute("COMMIT;")
            print(f"Usuario {user_id} reservó el asiento {seat_id} con éxito.")
            return True

    except Exception as e:
        print(f"Error al intentar reservar el asiento {seat_id} para el usuario {user_id}: {e}")
        cur.execute("ROLLBACK;")
        return False
    finally:
        cur.close()
