from base_datos.conexion import obtener_conexion

class ConductorDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    # 🔹 Insertar nuevo conductor con estado inicial
    def insertar(self, datos):
        query = """
            INSERT INTO Conductor (id_unidad, placa, nombre_conductor, estado)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            datos.get("id_unidad"),
            datos.get("placa"),
            datos.get("nombre_conductor"),
            datos.get("estado", "disponible")   # valor por defecto
        ))
        self.conn.commit()

    # 🔹 Eliminar conductor por ID
    def eliminar(self, id_conductor):
        query = "DELETE FROM Conductor WHERE id_conductor = ?"
        self.cursor.execute(query, (id_conductor,))
        self.conn.commit()

    # 🔹 Obtener todos los conductores (incluye estado)
    def obtener_todos(self):
        query = "SELECT * FROM Conductor"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]

    # 🔹 Actualizar datos de un conductor (incluye estado)
    def actualizar(self, datos):
        query = """
            UPDATE Conductor
            SET id_unidad = ?, placa = ?, nombre_conductor = ?, estado = ?
            WHERE id_conductor = ?
        """
        self.cursor.execute(query, (
            datos.get("id_unidad"),
            datos.get("placa"),
            datos.get("nombre_conductor"),
            datos.get("estado"),
            datos.get("id_conductor")
        ))
        self.conn.commit()

    # 🔹 Cambiar solo el estado de un conductor
    def actualizar_estado(self, id_conductor, nuevo_estado):
        query = "UPDATE Conductor SET estado = ? WHERE id_conductor = ?"
        self.cursor.execute(query, (nuevo_estado, id_conductor))
        self.conn.commit()