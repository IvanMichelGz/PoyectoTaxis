import pyodbc
from base_datos.conexion import obtener_conexion

class ViajeDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        query = "SELECT * FROM Viaje"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]

    def resumen_por_hora(self):
        query = """
            SELECT FORMAT(hora_salida, 'HH') AS hora, COUNT(*) AS total
            FROM Viaje
            GROUP BY FORMAT(hora_salida, 'HH')
            ORDER BY hora
        """
        self.cursor.execute(query)
        return {row[0]: row[1] for row in self.cursor.fetchall()}