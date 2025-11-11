from dao.viaje_dao import ViajeDAO

class ControladorViaje:
    def __init__(self):
        self.dao = ViajeDAO()

    def ver_todos_los_viajes(self):
        return self.dao.obtener_todos()

    def obtener_resumen_por_hora(self):
        return self.dao.resumen_por_hora()