import pyodbc
from base_datos.conexion import obtener_conexion

class ConductorDAO:
    def __init__(self):
        self.conn = obtener_conexion()
        self.cursor = self.conn.cursor()

    def insert(self, datos):
        query = "INSERT INTO Conductor (id_unidad, placa, nombre_conductor) VALUES (?, ?, ?)"
        self.cursor.execute(query, (
            datos["id_unidad"], datos["placa"], datos["nombre_conductor"]
        ))
        self.conn.commit()

    def eliminar(self, id_conductor):
        query = "DELETE FROM Conductor WHERE id_conductor = ?"
        self.cursor.execute(query, (id_conductor,))
        self.conn.commit()

    def obtener_todos(self):
        query = "SELECT * FROM Conductor"
        self.cursor.execute(query)
        columnas = [column[0] for column in self.cursor.description]
        return [dict(zip(columnas, row)) for row in self.cursor.fetchall()]