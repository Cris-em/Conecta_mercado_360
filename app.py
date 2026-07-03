# ----------------------------------------------------------------------
# IMPORTACIÓN DE BIBLIOTECAS Y MÓDULOS NECESARIOS
# ----------------------------------------------------------------------
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import re
import time
import traceback

# ----------------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS Y DIRECTORIOS DE LA APLICACIÓN
# ----------------------------------------------------------------------
# Obtenemos la ruta absoluta del directorio base del proyecto
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates') # Carpeta donde están los HTML

# Inicializamos la aplicación Flask
app = Flask(__name__, template_folder=template_dir, static_folder='static', static_url_path='/static')

# Clave secreta para proteger las sesiones y los mensajes flash (¡Cámbiala en producción!)
app.secret_key = 'tu_clave_secreta_aqui_cambiala_por_una_segura'

# ----------------------------------------------------------------------
# CONFIGURACIÓN DE LA SUBIDA DE ARCHIVOS (IMÁGENES)
# ----------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(base_dir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Crea la carpeta si no existe

# Función auxiliar para verificar si la extensión de un archivo es válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS (XAMPP / MYSQL)
# ----------------------------------------------------------------------
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',        # Usuario por defecto de XAMPP
        password='',        # Contraseña vacía por defecto en XAMPP
        database='conecta_mercado_360',
        port=3306,          # Puerto por defecto de MySQL
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5   # Tiempo de espera para evitar que la app se cuelgue
    )

# ----------------------------------------------------------------------
# INYECCIÓN GLOBAL DE BOTONES FLOTANTES (VOLVER E INICIO)
# ----------------------------------------------------------------------
@app.after_request
def inject_navigation_buttons(response):
    """
    Esta función se ejecuta después de que el servidor envíe cualquier página HTML.
    Si la página no tiene los botones, los añade automáticamente justo antes de cerrar el body.
    """
    if response.content_type and 'text/html' in response.content_type:
        html = response.get_data(as_text=True)
        if 'id="global-nav-buttons"' not in html:
            nav_html = '''
            <div id="global-nav-buttons" style="position: fixed; bottom: 20px; left: 20px; z-index: 9999; display: flex; gap: 12px; background: rgba(86, 0, 158, 0.95); backdrop-filter: blur(12px); padding: 8px 16px; border-radius: 60px; border: 2px solid #FF1493; box-shadow: 0 4px 12px rgba(86, 0, 158, 0.3);">
                <button id="global-btn-volver" style="background: #FF1493; border: none; color: white; font-family: 'Inter', sans-serif; font-weight: 600; padding: 8px 16px; border-radius: 40px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: 0.2s;">
                    <i class="fas fa-arrow-left"></i> Volver
                </button>
                <button id="global-btn-inicio" style="background: #FFC400; border: none; color: #2e1a30; font-family: 'Inter', sans-serif; font-weight: 600; padding: 8px 16px; border-radius: 40px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: 0.2s;">
                    <i class="fas fa-home"></i> Inicio
                </button>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var btnVolver = document.getElementById('global-btn-volver');
                    var btnInicio = document.getElementById('global-btn-inicio');
                    if (btnVolver) btnVolver.addEventListener('click', function() { window.history.back(); });
                    if (btnInicio) btnInicio.addEventListener('click', function() { window.location.href = '/'; });
                    document.querySelectorAll('#global-nav-buttons button').forEach(btn => {
                        btn.addEventListener('mouseenter', function() { this.style.transform = 'scale(1.05)'; });
                        btn.addEventListener('mouseleave', function() { this.style.transform = 'scale(1)'; });
                    });
                });
            </script>
            '''
            # Insertamos el HTML justo antes de la etiqueta de cierre </body>
            html = re.sub(r'</body>', nav_html + '</body>', html, flags=re.IGNORECASE)
            response.set_data(html)
    return response

# ============================================================================
# RUTAS PÚBLICAS (ACCESO SIN INICIAR SESIÓN)
# ============================================================================

# Página de inicio y login principal
@app.route('/')
def login_home():
    return render_template('login.html')

# Página de registro de nuevos usuarios
@app.route('/registro')
def pagina_registro():
    return render_template('registro.html')

# Página del modo invitado
@app.route('/invitado')
def pagina_invitado():
    return render_template('invitado.html')

# API pública que devuelve los datos (locales y productos) en formato JSON
@app.route('/api/datos_mercado')
def api_datos_mercado():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM locales")
            locales = cursor.fetchall()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
        conn.close()
        return jsonify({'locales': locales, 'productos': productos})
    except Exception as e:
        # Imprime el error en la terminal de VS Code para depuración
        print(f"ERROR EN API DATOS MERCADO: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# API para registrar un nuevo usuario
@app.route('/api/registrar_usuario', methods=['POST'])
def api_registrar_usuario():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol')
        
        if not nombre or not email or not password:
            return jsonify({'error': 'Faltan campos'}), 400
        
        # Se encripta la contraseña por seguridad
        hashed = generate_password_hash(password)
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Verificar si el correo ya existe en la base de datos
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                conn.close()
                return jsonify({'error': 'Correo ya registrado'}), 400
            
            # Insertar el nuevo usuario
            cursor.execute("INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (%s, %s, %s, %s)", (nombre, email, hashed, rol))
            user_id = cursor.lastrowid
            
            # Crear perfil vacío según el rol elegido
            if rol == 'vendedor':
                cursor.execute("INSERT INTO perfiles_vendedor (usuario_id) VALUES (%s)", (user_id,))
            elif rol == 'comprador':
                cursor.execute("INSERT INTO perfiles_comprador (usuario_id) VALUES (%s)", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Usuario registrado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API para iniciar sesión (normal y administrador)
@app.route('/api/iniciar_sesion', methods=['POST'])
def api_iniciar_sesion():
    try:
        data = request.get_json()
        usuario = data.get('usuario')  # Para normal es email, para admin es nombre
        password = data.get('password')
        is_admin = data.get('isAdmin', False)

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Si es admin, busca por nombre. Si no, busca por email.
            if is_admin:
                cursor.execute("SELECT id, nombre, contrasena, rol FROM usuarios WHERE nombre = %s", (usuario,))
            else:
                cursor.execute("SELECT id, nombre, contrasena, rol FROM usuarios WHERE email = %s", (usuario,))
            user = cursor.fetchone()
        conn.close()

        # Verificar si el usuario existe y la contraseña es correcta
        if user and check_password_hash(user['contrasena'], password):
            return jsonify({'success': True, 'id': user['id'], 'nombre': user['nombre'], 'rol': user['rol']})
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# RUTAS DEL COMPRADOR
# ============================================================================

@app.route('/comprador/inicio')
def comprador_inicio():
    return render_template('comprador_inicio.html')

@app.route('/comprador/carrito')
def comprador_carrito():
    return render_template('comprador_carrito.html')

@app.route('/comprador/mapa')
def comprador_mapa():
    return render_template('comprador_mapa.html')

@app.route('/usuario/perfil', methods=['GET', 'POST'])
def usuario_perfil():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nombre = request.form.get('fullName')
        email = request.form.get('email')
        direccion = request.form.get('address')
        telefono = request.form.get('phone')
        pago = request.form.get('payment')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Validar que el nuevo correo no esté siendo usado por otro usuario
            cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email, user_id))
            if cursor.fetchone():
                conn.close()
                flash("Error: El correo electrónico ya está registrado por otro usuario.", "error")
                return redirect(url_for('usuario_perfil'))
            
            cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s", (nombre, email, user_id))
            cursor.execute("UPDATE perfiles_comprador SET nombre = %s, direccion = %s, telefono = %s, metodo_pago = %s WHERE usuario_id = %s", (nombre, direccion, telefono, pago, user_id))
            
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename):
                    name, ext = os.path.splitext(secure_filename(file.filename))
                    foto_nombre = f"comprador_{int(time.time())}{ext}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_nombre))
                    cursor.execute("UPDATE usuarios SET foto_perfil = %s WHERE id = %s", (f'/static/uploads/{foto_nombre}', user_id))
        conn.commit()
        conn.close()
        flash("Perfil de comprador actualizado correctamente", "success")
        return redirect(url_for('usuario_perfil'))
    return render_template('usuario_perfil.html')

@app.route('/local/<int:local_id>')
def detalle_local(local_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM locales WHERE id = %s", (local_id,))
            local = cursor.fetchone()
            if not local:
                conn.close()
                return "Local no encontrado", 404
            cursor.execute("SELECT * FROM productos WHERE local_id = %s LIMIT 2", (local_id,))
            productos = cursor.fetchall()
        conn.close()
        return render_template('local_detalle.html', local=local, productos=productos)
    except Exception as e:
        return "Error interno", 500

# ============================================================================
# RUTAS DEL VENDEDOR
# ============================================================================

@app.route('/vendedor/inicio')
def vendedor_inicio():
    return render_template('vendedor_inicio.html')

@app.route('/vendedor/stock')
def vendedor_stock():
    return render_template('vendedor_stock.html')

@app.route('/vendedor/ventas')
def vendedor_ventas():
    return render_template('vendedor_ventas.html')

@app.route('/vendedor/perfil', methods=['GET', 'POST'])
def vendedor_perfil():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nombre = request.form.get('fullName')
        email = request.form.get('email')
        nombre_negocio = request.form.get('businessName')
        descripcion = request.form.get('businessDesc')
        ubicacion = request.form.get('sellerLocation')
        telefono = request.form.get('sellerPhone')

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email, user_id))
            if cursor.fetchone():
                conn.close()
                flash("Error: El correo electrónico ya está registrado por otro usuario.", "error")
                return redirect(url_for('vendedor_perfil'))
            
            cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s", (nombre, email, user_id))
            cursor.execute("UPDATE perfiles_vendedor SET nombre = %s, nombre_negocio = %s, descripcion = %s, ubicacion = %s, telefono = %s WHERE usuario_id = %s", (nombre, nombre_negocio, descripcion, ubicacion, telefono, user_id))
            
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename):
                    name, ext = os.path.splitext(secure_filename(file.filename))
                    foto_nombre = f"vendedor_{int(time.time())}{ext}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_nombre))
                    cursor.execute("UPDATE usuarios SET foto_perfil = %s WHERE id = %s", (f'/static/uploads/{foto_nombre}', user_id))
        conn.commit()
        conn.close()
        flash("Perfil de vendedor actualizado correctamente", "success")
        return redirect(url_for('vendedor_perfil'))
    return render_template('vendedor_perfil.html')

@app.route('/vendedor/subir-producto', methods=['GET', 'POST'])
def vendedor_subir():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        unidad = request.form.get('unidad')
        video_url = request.form.get('video_url')
        
        if not user_id:
            flash("Error: No se pudo identificar al usuario.", "error")
            return redirect(url_for('vendedor_subir'))
        
        imagen_url = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                nuevo_nombre = f"prod_{int(time.time())}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre))
                imagen_url = f'/static/uploads/{nuevo_nombre}'
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM locales WHERE usuario_id = %s", (user_id,))
                local = cursor.fetchone()
                if not local:
                    flash("Error: Debes crear un local (puesto) antes de subir productos.", "error")
                    return redirect(url_for('vendedor_inicio'))
                local_id = local['id']
                cursor.execute("INSERT INTO productos (local_id, nombre, descripcion, categoria, precio, stock, unidad, imagen_url, video_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (local_id, nombre, descripcion, categoria, precio, stock, unidad, imagen_url, video_url))
            conn.commit()
            flash("Producto guardado exitosamente.", "success")
            return redirect(url_for('vendedor_stock'))
        except Exception as e:
            flash("Error al guardar el producto.", "error")
            return redirect(url_for('vendedor_subir'))
        finally:
            conn.close()
    return render_template('subir_producto.html')

@app.route('/api/agregar_local', methods=['POST'])
def api_agregar_local():
    try:
        usuario_id = request.form.get('usuario_id')
        nombre_local = request.form.get('nombre_local')
        descripcion = request.form.get('descripcion')
        
        if not nombre_local or not usuario_id:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
        
        imagen_url = None
        if 'imagen_local' in request.files:
            file = request.files['imagen_local']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                nuevo_nombre = f"local_{int(time.time())}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre))
                imagen_url = f'/static/uploads/{nuevo_nombre}'
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO locales (nombre, descripcion, imagen_local, usuario_id) VALUES (%s, %s, %s, %s)", (nombre_local, descripcion, imagen_url, usuario_id))
        connection.commit()
        connection.close()
        return jsonify({'success': True, 'message': 'Local creado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendedor/stock_data')
def api_vendedor_stock_data():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no identificado'}), 401
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM locales WHERE usuario_id = %s", (user_id,))
            local = cursor.fetchone()
            if not local:
                return jsonify({'local_id': None, 'productos': []})
            cursor.execute("SELECT * FROM productos WHERE local_id = %s", (local['id'],))
            productos = cursor.fetchall()
        connection.close()
        return jsonify({'local_id': local['id'], 'productos': productos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:product_id>', methods=['PUT', 'DELETE'])
def api_gestion_producto(product_id):
    try:
        connection = get_db_connection()
        if request.method == 'DELETE':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM productos WHERE id = %s", (product_id,))
            connection.commit()
            connection.close()
            return jsonify({'success': True, 'message': 'Eliminado'})
        elif request.method == 'PUT':
            data = request.get_json()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock = %s, unidad = %s WHERE id = %s", (data['nombre'], data['precio'], data['stock'], data['unidad'], product_id))
            connection.commit()
            connection.close()
            return jsonify({'success': True, 'message': 'Actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ✅ RUTAS DEL ADMINISTRADOR (¡AQUÍ ESTÁ LA RUTA QUE FALTABA!)
# ============================================================================

# Página principal del Panel de Administración
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# Función auxiliar para verificar que quien hace la petición es realmente Admin
def verificar_admin(admin_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (admin_id,))
        user = cursor.fetchone()
    conn.close()
    return user and user['rol'] == 'admin'

# API: Obtener todos los usuarios
@app.route('/api/admin/usuarios', methods=['GET'])
def api_admin_usuarios_get():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol FROM usuarios ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# API: Editar o Eliminar un usuario específico
@app.route('/api/admin/usuarios/<int:user_id>', methods=['PUT', 'DELETE'])
def api_admin_usuarios_manage(user_id):
    admin_id = request.args.get('admin_id')
    if not verificar_admin(admin_id):
        return jsonify({'error': 'Acción no permitida. Debes ser administrador.'}), 403
    
    conn = get_db_connection()
    try:
        if request.method == 'DELETE':
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Usuario eliminado'})
        elif request.method == 'PUT':
            data = request.get_json()
            nombre = data.get('nombre')
            email = data.get('email')
            rol = data.get('rol')
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email, user_id))
                if cursor.fetchone():
                    conn.close()
                    return jsonify({'error': 'El correo electrónico ya está registrado por otro usuario.'}), 400
                cursor.execute("UPDATE usuarios SET nombre = %s, email = %s, rol = %s WHERE id = %s", (nombre, email, rol, user_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Usuario actualizado'})
    except Exception as e:
        if conn.open: conn.close()
        return jsonify({'error': str(e)}), 500

# API: Obtener todos los productos
@app.route('/api/admin/productos', methods=['GET'])
def api_admin_productos_get():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# API: Editar o Eliminar un producto específico
@app.route('/api/admin/productos/<int:prod_id>', methods=['PUT', 'DELETE'])
def api_admin_productos_manage(prod_id):
    admin_id = request.args.get('admin_id')
    if not verificar_admin(admin_id):
        return jsonify({'error': 'Acción no permitida. Debes ser administrador.'}), 403
        
    conn = get_db_connection()
    try:
        if request.method == 'DELETE':
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM productos WHERE id = %s", (prod_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Producto eliminado'})
        elif request.method == 'PUT':
            data = request.get_json()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock = %s, unidad = %s WHERE id = %s", (data['nombre'], data['precio'], data['stock'], data['unidad'], prod_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Producto actualizado'})
    except Exception as e:
        if conn.open: conn.close()
        return jsonify({'error': str(e)}), 500

# API: Obtener todos los locales
@app.route('/api/admin/locales', methods=['GET'])
def api_admin_locales_get():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locales ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# API: Editar o Eliminar un local específico
@app.route('/api/admin/locales/<int:loc_id>', methods=['PUT', 'DELETE'])
def api_admin_locales_manage(loc_id):
    admin_id = request.args.get('admin_id')
    if not verificar_admin(admin_id):
        return jsonify({'error': 'Acción no permitida. Debes ser administrador.'}), 403
        
    conn = get_db_connection()
    try:
        if request.method == 'DELETE':
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM locales WHERE id = %s", (loc_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Local eliminado'})
        elif request.method == 'PUT':
            data = request.get_json()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE locales SET nombre = %s, descripcion = %s WHERE id = %s", (data['nombre'], data['descripcion'], loc_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Local actualizado'})
    except Exception as e:
        if conn.open: conn.close()
        return jsonify({'error': str(e)}), 500

# API: Obtener todas las ventas
@app.route('/api/admin/ventas')
def api_admin_ventas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT p.id as pedido_id, p.fecha, p.estado, p.total, u.nombre as cliente_nombre FROM pedidos p JOIN usuarios u ON p.usuario_id = u.id ORDER BY p.id DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# ============================================================================
# APIS DE PROCESAMIENTO DE PEDIDOS Y VENTAS
# ============================================================================

@app.route('/api/procesar_pedido', methods=['POST'])
def api_procesar_pedido():
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        items = data.get('items')
        estado = data.get('estado')
        total = data.get('total')
        
        if not usuario_id or not items or not total:
            return jsonify({'error': 'Faltan datos del pedido'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for item in items:
            cursor.execute("SELECT stock, nombre FROM productos WHERE id = %s", (item['id'],))
            prod = cursor.fetchone()
            if not prod:
                return jsonify({'error': f'Producto {item["nombre"]} no encontrado'}), 400
            if prod['stock'] < item['cantidad']:
                return jsonify({'error': f'No hay suficiente stock de {prod["nombre"]}. Quedan {prod["stock"]} unidades.'}), 400
        
        cursor.execute("INSERT INTO pedidos (usuario_id, estado, total) VALUES (%s, %s, %s)", (usuario_id, estado, total))
        pedido_id = cursor.lastrowid
        
        for item in items:
            cursor.execute("INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", (pedido_id, item['id'], item['cantidad'], item['precio']))
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (item['cantidad'], item['id']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Pedido procesado con éxito', 'pedido_id': pedido_id})
    except Exception as e:
        if 'conn' in locals() and conn.open:
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/pedidos_usuario')
def api_pedidos_usuario():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no identificado'}), 401
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT p.id as pedido_id, p.fecha, p.estado, p.total, dp.producto_id, dp.cantidad, dp.precio_unitario, pr.nombre as producto_nombre FROM pedidos p JOIN detalles_pedido dp ON p.id = dp.pedido_id JOIN productos pr ON dp.producto_id = pr.id WHERE p.usuario_id = %s ORDER BY p.fecha DESC", (user_id,))
        resultados = cursor.fetchall()
        conn.close()
        pedidos = {}
        for row in resultados:
            pedido_id = row['pedido_id']
            if pedido_id not in pedidos:
                pedidos[pedido_id] = {'id': pedido_id, 'fecha': row['fecha'], 'estado': row['estado'], 'total': float(row['total']), 'productos': []}
            pedidos[pedido_id]['productos'].append({'nombre': row['producto_nombre'], 'cantidad': row['cantidad'], 'precio_unitario': float(row['precio_unitario'])})
        return jsonify({'pedidos': list(pedidos.values())})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendedor/ventas')
def api_vendedor_ventas():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no identificado'}), 401
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT p.id as pedido_id, p.fecha, p.estado, p.total, u.nombre as cliente_nombre, pr.nombre as producto_nombre, dp.cantidad, dp.precio_unitario FROM pedidos p JOIN detalles_pedido dp ON p.id = dp.pedido_id JOIN productos pr ON dp.producto_id = pr.id JOIN locales l ON pr.local_id = l.id JOIN usuarios u ON p.usuario_id = u.id WHERE l.usuario_id = %s ORDER BY p.fecha DESC", (user_id,))
        resultados = cursor.fetchall()
        conn.close()
        ventas = []
        for row in resultados:
            ventas.append({'pedido_id': row['pedido_id'], 'fecha': row['fecha'], 'estado': row['estado'], 'total': float(row['total']), 'cliente_nombre': row['cliente_nombre'], 'producto_nombre': row['producto_nombre'], 'cantidad': row['cantidad'], 'precio_unitario': float(row['precio_unitario'])})
        return jsonify({'ventas': ventas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendedor/actualizar_estado_pedido', methods=['POST'])
def api_vendedor_actualizar_estado_pedido():
    try:
        data = request.get_json()
        pedido_id = data.get('pedido_id')
        nuevo_estado = data.get('estado')
        user_id = data.get('user_id')
        
        if not pedido_id or not nuevo_estado or not user_id:
            return jsonify({'error': 'Faltan datos para actualizar el estado'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT l.usuario_id FROM pedidos p JOIN detalles_pedido dp ON p.id = dp.pedido_id JOIN productos pr ON dp.producto_id = pr.id JOIN locales l ON pr.local_id = l.id WHERE p.id = %s LIMIT 1", (pedido_id,))
        result = cursor.fetchone()
        if not result or int(result['usuario_id']) != int(user_id):
            conn.close()
            return jsonify({'error': 'No tienes permiso para modificar este pedido.'}), 403
        cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Estado del pedido actualizado a ' + nuevo_estado})
    except Exception as e:
        if 'conn' in locals() and conn.open:
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MANEJO DE ERRORES Y ARRANQUE DEL SERVIDOR
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Página no encontrada.</p>", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "<h1>500</h1><p>Error interno del servidor.</p>", 500

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciando en puerto 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)