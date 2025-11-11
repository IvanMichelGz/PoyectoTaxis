class Usuario:
    def __init__(self, nombre_alumno, usuario, password, rol, año_nacimiento,
                 correo, grupo, numero_cuenta, sexo, carrera):
        self.nombre_alumno = nombre_alumno
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.año_nacimiento = año_nacimiento
        self.correo = correo
        self.grupo = grupo
        self.numero_cuenta = numero_cuenta
        self.sexo = sexo
        self.carrera = carrera

    def to_dict(self):
        return {
            "nombre_alumno": self.nombre_alumno,
            "usuario": self.usuario,
            "password": self.password,
            "rol": self.rol,
            "año_nacimiento": self.año_nacimiento,
            "correo": self.correo,
            "grupo": self.grupo,
            "numero_cuenta": self.numero_cuenta,
            "sexo": self.sexo,
            "carrera": self.carrera
        }