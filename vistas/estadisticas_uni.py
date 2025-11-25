import flet as ft

def ver_estadisticas(page, viajes, volver_callback):
    """
    Muestra estadísticas de viajes en tarjetas con colores pastel.
    Incluye botón de volver al panel principal.
    """
    # Contar estados
    pendientes = sum(1 for v in viajes if v["estado"] == "pendiente")
    en_curso = sum(1 for v in viajes if v["estado"] == "en curso")
    finalizados = sum(1 for v in viajes if v["estado"] == "finalizado")

    # Tarjetas métricas
    metricas = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("🟡 Pendientes", weight=ft.FontWeight.BOLD),
                ft.Text(str(pendientes), size=22, weight=ft.FontWeight.W_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.AMBER_50, padding=16, border_radius=12, expand=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("🔵 En curso", weight=ft.FontWeight.BOLD),
                ft.Text(str(en_curso), size=22, weight=ft.FontWeight.W_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50, padding=16, border_radius=12, expand=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("✅ Finalizados", weight=ft.FontWeight.BOLD),
                ft.Text(str(finalizados), size=22, weight=ft.FontWeight.W_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREEN_50, padding=16, border_radius=12, expand=True
        ),
    ], spacing=12)

    # Layout principal con botón volver
    page.clean()
    page.add(
        ft.Column([
            ft.Text("📊 Estadísticas de viajes", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            metricas,
            ft.ElevatedButton("🔙 Volver", icon=ft.Icons.ARROW_BACK,
                              bgcolor=ft.Colors.GREY_200, color=ft.Colors.GREY_800,
                              on_click=lambda e: volver_callback(page))
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )