from base_datos.conexion import obtener_conexion

class UsuarioDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    def insert(self, datos):
        query = """
            INSERT INTO dbo.Usuario (
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
        query = "SELECT * FROM dbo.Usuario WHERE usuario = ? AND password = ?"
        self.cursor.execute(query, (usuario, password))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None

    def obtener_todos(self):
        query = "SELECT * FROM dbo.Usuario"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]

    def eliminar_por_usuario(self, usuario):
        query = "DELETE FROM dbo.Usuario WHERE usuario = ?"
        self.cursor.execute(query, (usuario,))
        self.conn.commit()

    def eliminar_por_id(self, id_usuario):
        # 🔄 corregido: usar id_usuario
        query = "DELETE FROM dbo.Usuario WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        self.conn.commit()

    def actualizar_usuario(self, datos):
        query = """
            UPDATE dbo.Usuario
            SET nombre_alumno = ?, correo = ?, grupo = ?, carrera = ?
            WHERE id_usuario = ?
        """
        self.cursor.execute(query, (
            datos["nombre_alumno"],
            datos["correo"],
            datos["grupo"],
            datos["carrera"],
            datos["id_usuario"]   # ← clave correcta
        ))
        self.conn.commit()

    def buscar_por_correo(self, correo):
        query = "SELECT * FROM dbo.Usuario WHERE correo = ?"
        self.cursor.execute(query, (correo,))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None

    def obtener_usuario_por_id(self, id_usuario):
        # 🔄 nuevo método para refrescar datos
        query = "SELECT * FROM dbo.Usuario WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None