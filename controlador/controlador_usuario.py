from dao.usuario_dao import UsuarioDAO

class ControladorUsuario:
    def __init__(self):
        self.dao = UsuarioDAO()

    def crear_usuario(self, datos):
        self.dao.insert(datos)

    def obtener_usuario_por_credenciales(self, usuario, password):
        return self.dao.obtener_por_credenciales(usuario, password)

    def obtener_todos(self):
        return self.dao.obtener_todos()