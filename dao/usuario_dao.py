import pyodbc
from base_datos.conexion import obtener_conexion

class UsuarioDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    def insert(self, datos):
        query = """
            INSERT INTO Usuario (
                nombre_alumno, usuario, password, rol,
                año_nacimiento, correo, grupo, numero_cuenta, sexo, carrera
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            datos["nombre_alumno"], datos["usuario"], datos["password"], datos["rol"],
            datos["año_nacimiento"], datos["correo"], datos["grupo"],
            datos["numero_cuenta"], datos["sexo"], datos["carrera"]
        ))
        self.conn.commit()

    def obtener_por_credenciales(self, usuario, password):
        query = "SELECT * FROM Usuario WHERE usuario = ? AND password = ?"
        self.cursor.execute(query, (usuario, password))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None

    def obtener_todos(self):
        query = "SELECT * FROM Usuario"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]