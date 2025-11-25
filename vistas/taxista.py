import flet as ft
from controlador.controlador_usuario import ControladorUsuario
from dao.viaje_dao import ViajeDAO
from vistas.componentes import card, titulo
from vistas.viajes_uni import mostrar_viajes
from vistas.mapa_ui import ver_mapa
from vistas.estadisticas_uni import ver_estadisticas

def taxista_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()
    controlador = ControladorUsuario()
    viaje_dao = ViajeDAO()

    # ---------- Helpers ----------
    def mostrar_mensaje(texto: str):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    def cambiar_estado(id_viaje, nuevo_estado):
        viaje_dao.actualizar_estado_viaje(id_viaje, nuevo_estado)
        mostrar_mensaje(f"🚖 Viaje {id_viaje} marcado como {nuevo_estado}")
        actualizar_viajes(None)

    def actualizar_viajes(e):
        viajes = viaje_dao.obtener_viajes_por_taxista(datos["id_usuario"])
        mostrar_viajes(page, viajes, cambiar_estado)

    # ---------- Menú hamburguesa ----------
    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[
            ft.PopupMenuItem(text="✏️ Modificar perfil", on_click=lambda e: mostrar_mensaje("Modificar perfil")),
            ft.PopupMenuItem(text="🔒 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ]
    )

    # ---------- Layout principal ----------
    page.add(
        ft.Column([
            ft.Row([
                titulo("🚖 Panel del Taxista", 26),
                ft.Container(content=menu, alignment=ft.alignment.center_right)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            # Tarjeta de información del taxista
            card(ft.Column([
                ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
                ft.Text(f"📧 {datos.get('correo', '')}", size=18),
                ft.Text(f"📞 {datos.get('telefono', '')}", size=18),
                ft.Text(f"🚗 {datos.get('placa', '')}", size=18),
                ft.Text(f"🆔 Unidad {datos.get('id_unidad', '')}", size=18)
            ], spacing=8), width=350, color=ft.Colors.BLUE_50),

            # Tarjeta de viajes
            card(ft.Column([
                ft.Text("📋 Tus viajes asignados", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.ElevatedButton("🔄 Actualizar lista", icon=ft.Icons.REFRESH, expand=True, on_click=actualizar_viajes)
            ], spacing=10)),

            # Tarjeta de opciones rápidas
            card(ft.Column([
                ft.Text("⚙️ Opciones rápidas", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.Row([
                    ft.ElevatedButton("📍 Ver mapa", icon=ft.Icons.MAP,
                                      on_click=lambda e: ver_mapa(page, volver_callback)),
                    ft.ElevatedButton("📊 Estadísticas", icon=ft.Icons.BAR_CHART,
                                      on_click=lambda e: ver_estadisticas(page,
                                                                          viaje_dao.obtener_viajes_por_taxista(datos["id_usuario"]),
                                                                          volver_callback))
                ], spacing=10)
            ], spacing=10))
        ], spacing=20, scroll=ft.ScrollMode.AUTO)
    )