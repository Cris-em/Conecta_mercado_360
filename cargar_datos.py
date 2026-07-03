"""
ConectaMercado 360 — Cargador de datos desde JSON a MySQL (XAMPP)
================================================================
Requisito previo:
    pip install pymysql

Uso:
    python cargar_datos.py

Asegúrate de que XAMPP esté corriendo (Apache + MySQL).
"""

import json
import sys
from pathlib import Path

try:
    import pymysql
except ImportError:
    print("[ERROR] pymysql no está instalado.")
    print("        Ejecuta: pip install pymysql")
    sys.exit(1)

# =============================================================
# CONFIGURACIÓN DE CONEXIÓN — Ajusta si es necesario
# =============================================================
DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     3306,
    "user":     "root",
    "password": "",               # XAMPP por defecto no tiene contraseña
    "database": "conecta_mercado_360",
    "charset":  "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

# Ruta base donde están los JSON (misma carpeta que este script / carpeta data/)
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


# =============================================================
# UTILIDAD: cargar JSON
# =============================================================
def cargar_json(nombre_archivo: str) -> list:
    ruta = DATA_DIR / nombre_archivo
    if not ruta.exists():
        print(f"  [WARN] Archivo no encontrado: {ruta}")
        return []
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# =============================================================
# CREAR TABLAS (idempotente — solo si no existen)
# =============================================================
CREAR_TABLAS = [
    # 1. locales (sin FK)
    """
    CREATE TABLE IF NOT EXISTS locales (
        id_local          INT           NOT NULL AUTO_INCREMENT,
        nombre_local      VARCHAR(100)  NOT NULL,
        ubicacion         VARCHAR(150)  NOT NULL,
        categoria         VARCHAR(80)   NOT NULL,
        metros_cuadrados  DECIMAL(6,2)  NOT NULL DEFAULT 0.00,
        renta_mensual     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        activo            TINYINT(1)    NOT NULL DEFAULT 1,
        PRIMARY KEY (id_local)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """,
    # 2. cliente
    """
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente       INT           NOT NULL AUTO_INCREMENT,
        nombre           VARCHAR(120)  NOT NULL,
        correo           VARCHAR(150)  NOT NULL UNIQUE,
        telefono         VARCHAR(20)   NOT NULL,
        direccion        VARCHAR(200)  NOT NULL,
        fecha_registro   DATE          NOT NULL,
        PRIMARY KEY (id_cliente)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """,
    # 3. empleado (FK -> locales)
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id_empleado        INT           NOT NULL AUTO_INCREMENT,
        nombre             VARCHAR(120)  NOT NULL,
        puesto             VARCHAR(80)   NOT NULL,
        salario            DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        fecha_contratacion DATE          NOT NULL,
        turno              ENUM('Matutino','Vespertino','Nocturno') NOT NULL DEFAULT 'Matutino',
        id_local           INT           NULL,
        PRIMARY KEY (id_empleado),
        CONSTRAINT fk_empleado_local FOREIGN KEY (id_local)
            REFERENCES locales(id_local) ON DELETE SET NULL ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """,
    # 4. productos (FK -> locales)
    """
    CREATE TABLE IF NOT EXISTS productos (
        id_producto      INT           NOT NULL AUTO_INCREMENT,
        nombre_producto  VARCHAR(120)  NOT NULL,
        descripcion      TEXT          NULL,
        precio           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        stock            INT           NOT NULL DEFAULT 0,
        unidad           VARCHAR(40)   NOT NULL DEFAULT 'pieza',
        categoria        VARCHAR(80)   NOT NULL,
        id_local         INT           NULL,
        PRIMARY KEY (id_producto),
        CONSTRAINT fk_producto_local FOREIGN KEY (id_local)
            REFERENCES locales(id_local) ON DELETE SET NULL ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """,
]


# =============================================================
# INSERTAR CON ON DUPLICATE KEY UPDATE (upsert)
# =============================================================
def insertar_locales(cursor, registros):
    sql = """
        INSERT INTO locales
            (id_local, nombre_local, ubicacion, categoria, metros_cuadrados, renta_mensual, activo)
        VALUES
            (%(id_local)s, %(nombre_local)s, %(ubicacion)s, %(categoria)s,
             %(metros_cuadrados)s, %(renta_mensual)s, %(activo)s)
        ON DUPLICATE KEY UPDATE
            nombre_local     = VALUES(nombre_local),
            ubicacion        = VALUES(ubicacion),
            categoria        = VALUES(categoria),
            metros_cuadrados = VALUES(metros_cuadrados),
            renta_mensual    = VALUES(renta_mensual),
            activo           = VALUES(activo);
    """
    # Convertir bool a int para MySQL
    for r in registros:
        r["activo"] = int(r["activo"])
    cursor.executemany(sql, registros)
    return cursor.rowcount


def insertar_clientes(cursor, registros):
    sql = """
        INSERT INTO cliente
            (id_cliente, nombre, correo, telefono, direccion, fecha_registro)
        VALUES
            (%(id_cliente)s, %(nombre)s, %(correo)s, %(telefono)s,
             %(direccion)s, %(fecha_registro)s)
        ON DUPLICATE KEY UPDATE
            nombre         = VALUES(nombre),
            correo         = VALUES(correo),
            telefono       = VALUES(telefono),
            direccion      = VALUES(direccion),
            fecha_registro = VALUES(fecha_registro);
    """
    cursor.executemany(sql, registros)
    return cursor.rowcount


def insertar_empleados(cursor, registros):
    sql = """
        INSERT INTO empleado
            (id_empleado, nombre, puesto, salario, fecha_contratacion, turno, id_local)
        VALUES
            (%(id_empleado)s, %(nombre)s, %(puesto)s, %(salario)s,
             %(fecha_contratacion)s, %(turno)s, %(id_local)s)
        ON DUPLICATE KEY UPDATE
            nombre             = VALUES(nombre),
            puesto             = VALUES(puesto),
            salario            = VALUES(salario),
            fecha_contratacion = VALUES(fecha_contratacion),
            turno              = VALUES(turno),
            id_local           = VALUES(id_local);
    """
    cursor.executemany(sql, registros)
    return cursor.rowcount


def insertar_productos(cursor, registros):
    sql = """
        INSERT INTO productos
            (id_producto, nombre_producto, descripcion, precio, stock, unidad, categoria, id_local)
        VALUES
            (%(id_producto)s, %(nombre_producto)s, %(descripcion)s, %(precio)s,
             %(stock)s, %(unidad)s, %(categoria)s, %(id_local)s)
        ON DUPLICATE KEY UPDATE
            nombre_producto = VALUES(nombre_producto),
            descripcion     = VALUES(descripcion),
            precio          = VALUES(precio),
            stock           = VALUES(stock),
            unidad          = VALUES(unidad),
            categoria       = VALUES(categoria),
            id_local        = VALUES(id_local);
    """
    cursor.executemany(sql, registros)
    return cursor.rowcount


# =============================================================
# MAIN
# =============================================================
def main():
    print("=" * 60)
    print("  ConectaMercado 360 — Cargador de datos JSON → MySQL")
    print("=" * 60)

    # 1. Conectar
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print(f"\n✅  Conexión exitosa a '{DB_CONFIG['database']}' en {DB_CONFIG['host']}")
    except pymysql.OperationalError as e:
        print(f"\n❌  No se pudo conectar a MySQL: {e}")
        print("     Verifica que XAMPP esté corriendo y los datos en DB_CONFIG sean correctos.")
        sys.exit(1)

    with conn:
        with conn.cursor() as cur:

            # 2. Crear tablas
            print("\n📋  Creando / verificando tablas...")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for ddl in CREAR_TABLAS:
                cur.execute(ddl)
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            print("     Tablas listas.")

            # 3. Cargar JSONs
            print("\n📂  Cargando archivos JSON desde:", DATA_DIR)

            locales   = cargar_json("locales.json")
            clientes  = cargar_json("clientes.json")
            empleados = cargar_json("empleados.json")
            productos = cargar_json("productos.json")

            # 4. Insertar en orden correcto (respetando FK)
            print("\n⬆️   Insertando datos...\n")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")

            if locales:
                n = insertar_locales(cur, locales)
                print(f"     locales   → {len(locales)} registros procesados (filas afectadas: {n})")

            if clientes:
                n = insertar_clientes(cur, clientes)
                print(f"     clientes  → {len(clientes)} registros procesados (filas afectadas: {n})")

            if empleados:
                n = insertar_empleados(cur, empleados)
                print(f"     empleados → {len(empleados)} registros procesados (filas afectadas: {n})")

            if productos:
                n = insertar_productos(cur, productos)
                print(f"     productos → {len(productos)} registros procesados (filas afectadas: {n})")

            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()

            # 5. Verificación
            print("\n📊  Conteo final:")
            for tabla in ["locales", "cliente", "empleado", "productos"]:
                cur.execute(f"SELECT COUNT(*) AS total FROM {tabla};")
                total = cur.fetchone()["total"]
                print(f"     {tabla:<12} → {total} filas")

    print("\n✅  ¡Proceso completado exitosamente!\n")


if __name__ == "__main__":
    main()
