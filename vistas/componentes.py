import flet as ft

def card(content, width=350, color=ft.Colors.WHITE):
    return ft.Container(
        content=content,
        bgcolor=color,
        padding=20,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=width,
        margin=10
    )

def titulo(texto, size=24, color=ft.Colors.BLUE_900):
    return ft.Text(texto, size=size, weight=ft.FontWeight.BOLD, color=color)