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
    
    def eliminar_por_usuario(self, usuario):
        self.dao.eliminar_por_usuario(usuario)

    # Si usas ID como clave primaria:
    def eliminar_por_id(self, id_usuario):
        self.dao.eliminar_por_id(id_usuario)
        
    def actualizar_usuario(self, datos):
        self.dao.actualizar_usuario(datos)

    # 🔄 Nuevo método para refrescar datos
    def obtener_usuario_por_id(self, id_usuario):
        return self.dao.obtener_usuario_por_id(id_usuario)