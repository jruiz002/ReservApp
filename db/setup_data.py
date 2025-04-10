def setup_simulacion(conn, cantidad_asientos):
    try:
        cur = conn.cursor()

        # Limpiar reservas
        cur.execute("DELETE FROM Reservas;")
        # Reiniciar estado de asientos a FALSE
        cur.execute("UPDATE Asientos SET estado = FALSE;")

        # Ver cuántos asientos existen actualmente
        cur.execute("SELECT COUNT(*) FROM Asientos;")
        actuales = cur.fetchone()[0]
        faltantes = cantidad_asientos - actuales

        # Insertar los asientos que hagan falta
        if faltantes > 0:
            for _ in range(faltantes):
                cur.execute("INSERT INTO Asientos (estado) VALUES (FALSE);")
            print(f"[INFO] Se insertaron {faltantes} nuevos asientos.")
        else:
            print("[INFO] Cantidad de asientos suficiente.\n")
        conn.commit()
        cur.close()

    except Exception as e:
        print(f"[ERROR] al preparar la simulación: {e}")
        conn.rollback()
