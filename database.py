import sqlite3

def create_connection():
    """Crea y retorna una conexión a la base de datos."""
    return sqlite3.connect("gestor_multitiempo.db")

def drop_table():
    """Elimina la tabla 'usuarios' si existe."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    connection.commit()
    connection.close()

def create_tables():
    """Crea la tabla 'usuarios' si no existe."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def add_user(nombre_usuario, contrasena):
    """Añade un nuevo usuario a la tabla 'usuarios'."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, contrasena))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Error: El nombre de usuario '{nombre_usuario}' ya está en uso.")
    connection.close()

def get_user(nombre_usuario):
    """Obtiene un usuario de la tabla 'usuarios' por su nombre de usuario."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
    user = cursor.fetchone()
    connection.close()
    return user
