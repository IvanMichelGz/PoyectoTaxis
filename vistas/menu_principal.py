import flet as ft

def menu_principal(page: ft.Page, iniciar_sesion, crear_cuenta, navegar_callback):
    page.clean()
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🚕 Bienvenido a Agenda de Taxis", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona una opción:", size=20),
                ft.ElevatedButton("🔐 Iniciar sesión", on_click=lambda e: iniciar_sesion(page, menu_principal, crear_cuenta, navegar_callback)),
                ft.ElevatedButton("📝 Crear cuenta", on_click=lambda e: crear_cuenta(page, menu_principal, iniciar_sesion,navegar_callback))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            alignment=ft.alignment.center,
            expand=True,
            padding=20
        )
    )