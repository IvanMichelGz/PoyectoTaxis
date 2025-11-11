class Conductor:
    def __init__(self, id_unidad, placa, nombre_conductor):
        self.id_unidad = id_unidad
        self.placa = placa
        self.nombre_conductor = nombre_conductor

    def to_dict(self):
        return {
            "id_unidad": self.id_unidad,
            "placa": self.placa,
            "nombre_conductor": self.nombre_conductor
        }