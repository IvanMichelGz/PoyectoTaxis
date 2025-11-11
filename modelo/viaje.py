class Viaje:
    def __init__(self, id_viaje, destino, tarifa, estado, hora_salida):
        self.id_viaje = id_viaje
        self.destino = destino
        self.tarifa = tarifa
        self.estado = estado
        self.hora_salida = hora_salida

    def to_dict(self):
        return {
            "id_viaje": self.id_viaje,
            "destino": self.destino,
            "tarifa": self.tarifa,
            "estado": self.estado,
            "hora_salida": self.hora_salida
        }