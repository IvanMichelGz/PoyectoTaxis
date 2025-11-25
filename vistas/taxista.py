import flet as ft
from controlador.controlador_usuario import ControladorUsuario

def taxista_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()

    controlador = ControladorUsuario()

    # Datos iniciales del taxista
    nombre = datos.get("nombre_alumno", "Taxista")
    placa = datos.get("placa", "Sin placa")
    telefono = datos.get("telefono", "Sin teléfono")
    correo = datos.get("correo", "Sin correo")
    id_unidad = datos.get("id_unidad", "N/A")

    # Función utilitaria para mostrar SnackBar
    def mostrar_mensaje(texto: str):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    # 🔹 Vista de edición de perfil
    def modificar_perfil(e):
        page.clean()

        nombre_field = ft.TextField(label="Nombre", value=nombre, width=300)
        correo_field = ft.TextField(label="Correo", value=correo, width=300)
        telefono_field = ft.TextField(label="Teléfono", value=telefono, width=300)
        placa_field = ft.TextField(label="Placa", value=placa, width=300)
        unidad_field = ft.TextField(label="Unidad", value=str(id_unidad), width=300)

        def guardar_cambios(ev):
            nuevos_datos = {
                "id_usuario": datos["id_usuario"],
                "nombre_alumno": nombre_field.value,
                "correo": correo_field.value,
                "telefono": telefono_field.value,
                "placa": placa_field.value,
                "id_unidad": unidad_field.value
            }
            controlador.actualizar_usuario(nuevos_datos)
            mostrar_mensaje("✅ Perfil actualizado correctamente")
            taxista_view(page, nuevos_datos, volver_callback)

        page.add(
            ft.Column([
                ft.Text("✏️ Modificar perfil", size=24, weight=ft.FontWeight.BOLD),
                nombre_field,
                correo_field,
                telefono_field,
                placa_field,
                unidad_field,
                ft.Row([
                    ft.ElevatedButton("💾 Guardar", on_click=guardar_cambios),
                    ft.ElevatedButton("❌ Cancelar", on_click=lambda e: taxista_view(page, datos, volver_callback))
                ], spacing=10)
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
        )

    # 🔹 Menú hamburguesa
    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[
            ft.PopupMenuItem(text="✏️ Modificar perfil", on_click=modificar_perfil),
            ft.PopupMenuItem(text="🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ]
    )

    # Encabezado con menú
    header = ft.Row(
        controls=[
            ft.Text("🚖 Panel del Taxista", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Container(content=menu, alignment=ft.alignment.center_right)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Tarjeta de información del taxista
    info_card = ft.Container(
        content=ft.Column([
            ft.Text(f"👤 Nombre: {nombre}", size=18),
            ft.Text(f"📧 Correo: {correo}", size=18),
            ft.Text(f"📞 Teléfono: {telefono}", size=18),
            ft.Text(f"🚗 Placa: {placa}", size=18),
            ft.Text(f"🆔 Unidad: {id_unidad}", size=18)
        ], spacing=8),
        bgcolor=ft.Colors.BLUE_50,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=400,
        margin=10
    )

    # Tarjeta de viajes
    viajes_card = ft.Container(
        content=ft.Column([
            ft.Text("📋 Tus viajes asignados", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Text("Aquí aparecerán los viajes pendientes, en curso o finalizados."),
            ft.ElevatedButton("🔄 Actualizar lista", icon=ft.Icons.REFRESH, expand=True)
        ], spacing=10),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=400,
        margin=10
    )

    # Tarjeta de opciones rápidas
    opciones_card = ft.Container(
        content=ft.Column([
            ft.Text("⚙️ Opciones rápidas", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Row([
                ft.ElevatedButton("📍 Ver mapa", icon=ft.Icons.MAP),
                ft.ElevatedButton("📊 Estadísticas", icon=ft.Icons.BAR_CHART)
            ], spacing=10)
        ], spacing=10),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=400,
        margin=10
    )

    # Layout principal
    page.add(
        ft.Column([
            header,
            info_card,
            ft.Row([viajes_card, opciones_card], alignment=ft.MainAxisAlignment.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        spacing=20)
    )