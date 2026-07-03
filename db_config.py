"""
ConectaMercado 360 — Módulo de conexión reutilizable
=====================================================
Importa este módulo en tu app Flask para obtener conexiones.

Uso en Flask:
    from db_config import get_connection

    @app.route('/clientes')
    def lista_clientes():
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cliente")
            clientes = cur.fetchall()
        conn.close()
        return jsonify(clientes)
"""

import pymysql
import pymysql.cursors


# =============================================================
# CONFIGURACIÓN CENTRAL — modifica solo aquí si cambia algo
# =============================================================
DB_HOST     = "127.0.0.1"
DB_PORT     = 3306
DB_USER     = "root"
DB_PASSWORD = ""                     # XAMPP: sin contraseña por defecto
DB_NAME     = "conecta_mercado_360"
DB_CHARSET  = "utf8mb4"


def get_connection() -> pymysql.connections.Connection:
    """
    Devuelve una nueva conexión a MySQL (XAMPP).
    Usa DictCursor para obtener resultados como diccionarios.
    """
    return pymysql.connect(
        host       = DB_HOST,
        port       = DB_PORT,
        user       = DB_USER,
        password   = DB_PASSWORD,
        database   = DB_NAME,
        charset    = DB_CHARSET,
        cursorclass= pymysql.cursors.DictCursor,
        autocommit = False,
    )


def test_conexion():
    """Prueba rápida de conexión. Ejecuta este archivo directamente para verificar."""
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS version;")
            ver = cur.fetchone()
            print(f"✅  Conexión exitosa — MySQL versión: {ver['version']}")

            # Resumen de tablas
            cur.execute("SHOW TABLES;")
            tablas = cur.fetchall()
            print(f"     Tablas encontradas en '{DB_NAME}':")
            for t in tablas:
                nombre = list(t.values())[0]
                cur.execute(f"SELECT COUNT(*) AS n FROM `{nombre}`;")
                n = cur.fetchone()["n"]
                print(f"       • {nombre:<20} {n} filas")
        conn.close()
    except pymysql.OperationalError as e:
        print(f"❌  Error de conexión: {e}")
        print("     Verifica que XAMPP (MySQL) esté activo.")


if __name__ == "__main__":
    test_conexion()
