import flet as ft

def taxista_view(page: ft.Page, nombre: str, volver_callback):
    page.clean()
    page.add(
        ft.Column([
            ft.Text(f"🚖 Panel del Taxista: {nombre}", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Tus viajes asignados aparecerán aquí."),
            ft.ElevatedButton("🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    )