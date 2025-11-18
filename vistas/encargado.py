import flet as ft

def encargado_view(page: ft.Page, nombre: str, volver_callback):
    page.clean()
    page.add(
        ft.Column([
            ft.Text(f"🧑‍💼 Panel del Encargado: {nombre}", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Aquí puedes administrar taxis y ver estadísticas."),
            ft.ElevatedButton("🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    )