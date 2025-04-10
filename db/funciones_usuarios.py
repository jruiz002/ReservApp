import psycopg2

def get_first_n_users(conn, n):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM Usuarios ORDER BY id_usuario LIMIT %s;", (n,))
        rows = cur.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        cur.close()
