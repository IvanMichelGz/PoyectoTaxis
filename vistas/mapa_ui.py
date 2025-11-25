import flet as ft

def tarjeta_base_taxi(nombre, ubicacion, horario, rating, url_maps, page):
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.CircleAvatar(
                    bgcolor=ft.Colors.BLUE_200,
                    content=ft.Icon(ft.Icons.LOCAL_TAXI, color=ft.Colors.BLUE_900),
                    radius=20
                ),
                ft.Text(nombre, size=18, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            ft.Row([ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED_400), ft.Text(ubicacion)], spacing=6),
            ft.Row([ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.BLUE_400), ft.Text(horario)], spacing=6),
            ft.Row([ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER), ft.Text(rating)], spacing=6),
            ft.ElevatedButton("🌐 Abrir en Maps", icon=ft.Icons.MAP,
                              on_click=lambda e: page.launch_url(url_maps),
                              bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_900)
        ], spacing=8),
        bgcolor=ft.Colors.WHITE,
        padding=16,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=280,
        margin=10
    )

def ver_mapa(page, volver_callback):
    page.clean()
    page.add(
        ft.Column([
            ft.Text("🗺️ Bases de taxis cercanas", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Row([
                tarjeta_base_taxi("Concepción Chico", "San Felipe del Progreso", "6:00 AM - 10:00 PM", "⭐ 4.8",
                                  "https://maps.google.com?q=Concepcion+Chico", page),
                tarjeta_base_taxi("Base Atlacomulco", "Av. José María Morelos 102", "24 horas", "⭐ 5.0",
                                  "https://maps.google.com?q=Base+Atlacomulco", page),
                tarjeta_base_taxi("Tepetitlán - Tungareo", "Cobertura regional", "7:00 AM - 9:00 PM", "⭐ 4.5",
                                  "https://maps.google.com?q=Tepetitlan+Tungareo", page)
            ], wrap=True, spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.ElevatedButton("🔙 Volver", icon=ft.Icons.ARROW_BACK,
                              bgcolor=ft.Colors.GREY_200, color=ft.Colors.GREY_800,
                              on_click=lambda e: volver_callback(page))
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )