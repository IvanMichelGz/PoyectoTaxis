import flet as ft

def alumno_view(page: ft.Page, nombre: str, volver_callback):
    page.clean()
    page.add(
        ft.Column([
            ft.Text(f"👨‍🎓 Bienvenido, {nombre}", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Aquí verás tus viajes asignados."),
            ft.ElevatedButton(
                "Volver al menú",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: volver_callback(page)
            )]
        )
    )