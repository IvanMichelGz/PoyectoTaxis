from dao.conductor_dao import ConductorDAO

class ControladorConductor:
    def __init__(self):
        self.dao = ConductorDAO()

    def crear_conductor(self, datos):
        self.dao.insert(datos)

    def eliminar_conductor(self, id_conductor):
        self.dao.eliminar(id_conductor)

    def obtener_todos(self):
        return self.dao.obtener_todos()