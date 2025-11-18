import flet as ft
from controlador.controlador_usuario import ControladorUsuario
from controlador.controlador_conductor import ControladorConductor
from controlador.controlador_viaje import ControladorViaje

from vistas.menu_principal import menu_principal
from vistas.iniciar_secion import iniciar_sesion
from vistas.crear_cuenta import crear_cuenta
from vistas.alumno import alumno_view
from vistas.taxista import taxista_view
from vistas.encargado import encargado_view

controlador_usuario = ControladorUsuario()
controlador_conductor = ControladorConductor()
controlador_viaje = ControladorViaje()

def main(page: ft.Page):
    page.title = "Agenda de Taxis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def navegar(page, datos,menu_principal, crear_cuenta):
        rol=datos["rol"]
        nombre=datos["nombre_alumno"]
        vistas = {
            "alumno": alumno_view,
            "taxista": taxista_view,
            "encargado": encargado_view
        }
        if rol in vistas:
            vistas[rol](page, nombre,lambda p: menu_principal(p,iniciar_sesion,crear_cuenta,navegar))

    menu_principal(page, iniciar_sesion, crear_cuenta, navegar)

ft.app(target=main)