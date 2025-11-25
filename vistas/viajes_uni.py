import flet as ft

def render_item_viaje(viaje, cambiar_estado):
    return ft.Row(
        [
            ft.Text(f"📍 Destino: {viaje['destino']} | Estado: {viaje['estado']}", size=16),
            ft.ElevatedButton(
                "▶ Iniciar",
                on_click=lambda e: cambiar_estado(viaje["id_viaje"], "en curso"),
                bgcolor=ft.Colors.BLUE_100,
                color=ft.Colors.BLUE_900
            ),
            ft.ElevatedButton(
                "✅ Finalizar",
                on_click=lambda e: cambiar_estado(viaje["id_viaje"], "finalizado"),
                bgcolor=ft.Colors.GREEN_100,
                color=ft.Colors.GREEN_900
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

def mostrar_viajes(page: ft.Page, viajes: list, cambiar_estado):
    if viajes:
        lista = ft.Column(
            [render_item_viaje(v, cambiar_estado) for v in viajes],
            spacing=10
        )
        page.add(lista)
    else:
        page.add(ft.Text("No tienes viajes asignados", color=ft.Colors.GREY_700))