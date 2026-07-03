from werkzeug.security import generate_password_hash
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='conecta_mercado_360', port=3306)
cursor = conn.cursor()
nombre = "Admin Principal"
email = "admin@conecta.com"
password = generate_password_hash("Admin123")
try:
    cursor.execute("INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (%s, %s, %s, %s)", (nombre, email, password, "admin"))
    conn.commit()
    print("✅ Admin creado. Usuario: 'Admin Principal', Contraseña: 'Admin123'")
except: print("⚠️ El admin ya existía.")
conn.close()