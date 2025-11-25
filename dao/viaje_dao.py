import pyodbc
from base_datos.conexion import obtener_conexion

class ViajeDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    # 🔹 Obtener todos los viajes
    def obtener_todos(self):
        query = "SELECT * FROM Viaje"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]

    # 🔹 Obtener viajes asignados a un conductor (usando id_usuario)
    def obtener_viajes_por_taxista(self, id_usuario):
        query = """
            SELECT id_viaje, destino, estado
            FROM Viaje
            WHERE id_usuario = ?
            ORDER BY id_viaje DESC
        """
        self.cursor.execute(query, (id_usuario,))
        rows = self.cursor.fetchall()
        columnas = [col[0] for col in self.cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    # 🔹 Actualizar estado de un viaje
    def actualizar_estado_viaje(self, id_viaje, nuevo_estado):
        query = "UPDATE Viaje SET estado = ? WHERE id_viaje = ?"
        self.cursor.execute(query, (nuevo_estado, id_viaje))
        self.conn.commit()

    # 🔹 Resumen de viajes por estado
    def resumen_por_estado(self):
        query = """
            SELECT estado, COUNT(*) AS total
            FROM Viaje
            GROUP BY estado
        """
        self.cursor.execute(query)
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    # 🔹 Eliminar viaje por ID
    def eliminar_por_id(self, id_viaje):
        query = "DELETE FROM Viaje WHERE id_viaje = ?"
        self.cursor.execute(query, (id_viaje,))
        self.conn.commit()

    # 🔹 Insertar nuevo viaje (mínimo viable)
    def insertar_viaje(self, datos):
        query = """
            INSERT INTO Viaje (destino, id_usuario, id_conductor, estado)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            datos.get("destino"),
            datos.get("id_usuario"),
            datos.get("id_conductor"),
            datos.get("estado", "pendiente")
        ))
        self.conn.commit()