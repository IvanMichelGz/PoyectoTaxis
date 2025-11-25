from base_datos.conexion import obtener_conexion

class UsuarioDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    # 🔹 Insertar nuevo usuario (flexible según rol)
    def insert(self, datos):
        query = """
            INSERT INTO dbo.Usuario (
                nombre_alumno, usuario, password, rol,
                año_nacimiento, correo, grupo, numero_cuenta, sexo, carrera,
                placa, id_unidad, puesto, telefono, direccion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            datos.get("nombre_alumno"),
            datos.get("usuario"),
            datos.get("password"),
            datos.get("rol"),
            datos.get("año_nacimiento"),
            datos.get("correo"),
            datos.get("grupo"),
            datos.get("numero_cuenta"),
            datos.get("sexo"),
            datos.get("carrera"),
            datos.get("placa"),
            datos.get("id_unidad"),
            datos.get("puesto"),
            datos.get("telefono"),
            datos.get("direccion")
        ))
        self.conn.commit()

    # 🔹 Obtener usuario por credenciales (login)
    def obtener_por_credenciales(self, usuario, password):
        query = "SELECT * FROM dbo.Usuario WHERE usuario = ? AND password = ?"
        self.cursor.execute(query, (usuario, password))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None

    # 🔹 Obtener todos los usuarios
    def obtener_todos(self):
        query = "SELECT * FROM dbo.Usuario"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]

    # 🔹 Eliminar por usuario
    def eliminar_por_usuario(self, usuario):
        query = "DELETE FROM dbo.Usuario WHERE usuario = ?"
        self.cursor.execute(query, (usuario,))
        self.conn.commit()

    # 🔹 Eliminar por ID
    def eliminar_por_id(self, id_usuario):
        query = "DELETE FROM dbo.Usuario WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        self.conn.commit()

    # 🔹 Actualizar usuario (según rol, campos opcionales)
    def actualizar_usuario(self, datos):
        query = """
            UPDATE dbo.Usuario
            SET nombre_alumno = ?, correo = ?, grupo = ?, carrera = ?,
                placa = ?, id_unidad = ?, puesto = ?, telefono = ?, direccion = ?
            WHERE id_usuario = ?
        """
        self.cursor.execute(query, (
            datos.get("nombre_alumno"),
            datos.get("correo"),
            datos.get("grupo"),
            datos.get("carrera"),
            datos.get("placa"),
            datos.get("id_unidad"),
            datos.get("puesto"),
            datos.get("telefono"),
            datos.get("direccion"),
            datos.get("id_usuario")
        ))
        self.conn.commit()

    # 🔹 Buscar usuario por correo
    def buscar_por_correo(self, correo):
        query = "SELECT * FROM dbo.Usuario WHERE correo = ?"
        self.cursor.execute(query, (correo,))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None

    # 🔹 Obtener usuario por ID
    def obtener_usuario_por_id(self, id_usuario):
        query = "SELECT * FROM dbo.Usuario WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        row = self.cursor.fetchone()
        if row:
            columnas = [column[0] for column in self.cursor.description]
            return dict(zip(columnas, row))
        return None