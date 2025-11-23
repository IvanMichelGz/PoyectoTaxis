import flet as ft
from controlador.controlador_usuario import ControladorUsuario

controlador_usuario = ControladorUsuario()

def alumno_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()

    # Inicializa SnackBar
    page.snack_bar = ft.SnackBar(content=ft.Text(""))

    def mostrar_snack(texto):
        page.snack_bar.content = ft.Text(texto)
        page.snack_bar.open = True
        page.update()

    def cerrar_dialogo():
        page.dialog.open = False
        page.update()

    def eliminar_cuenta(e):
        def confirmar():
            controlador_usuario.eliminar_por_id(datos["id_usuario"])
            mostrar_snack("✅ Cuenta eliminada")
            volver_callback(page)

        page.dialog = ft.AlertDialog(
            title=ft.Text("¿Eliminar cuenta?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
                ft.TextButton("Sí", on_click=lambda e: confirmar())
            ]
        )
        page.dialog.open = True
        page.update()

    def modificar_cuenta(e):
        page.clean()

        nombre_input = ft.TextField(label="Nombre", value=datos.get("nombre_alumno", ""))
        correo_input = ft.TextField(label="Correo", value=datos.get("correo", ""))
        grupo_input = ft.TextField(label="Grupo", value=datos.get("grupo", ""))
        carrera_input = ft.TextField(label="Carrera", value=datos.get("carrera", ""))

        def guardar_cambios(ev):
            nuevos_datos = {
                "id_usuario": datos["id_usuario"],
                "nombre_alumno": nombre_input.value,
                "correo": correo_input.value,
                "grupo": grupo_input.value,
                "carrera": carrera_input.value
            }
            controlador_usuario.actualizar_usuario(nuevos_datos)

            # 🔄 Recargar datos desde la base para reflejar cambios
            datos_actualizados = controlador_usuario.obtener_usuario_por_id(datos["id_usuario"])

            mostrar_snack("✏️ Cambios guardados")
            alumno_view(page, datos_actualizados, volver_callback)  # reconstruye la vista con datos frescos

        formulario = ft.Container(
            content=ft.Column([
                ft.Text("✏️ Modificar cuenta", size=24, weight=ft.FontWeight.BOLD),
                nombre_input,
                correo_input,
                grupo_input,
                carrera_input,
                ft.Row([
                    ft.ElevatedButton("Guardar cambios", icon=ft.Icons.SAVE, on_click=guardar_cambios, expand=True),
                    ft.ElevatedButton("Eliminar cuenta", icon=ft.Icons.DELETE, on_click=eliminar_cuenta, expand=True),
                    ft.ElevatedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=lambda e: volver_callback(page), expand=True)
                ], spacing=10)
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
            alignment=ft.alignment.center,
            width=500
        )

        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[formulario],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.WHITE,
                expand=True
            )
        )

    def cerrar_sesion(e):
        volver_callback(page)

    menu_usuario = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        tooltip="Opciones de cuenta",
        items=[
            ft.PopupMenuItem(text="✏️ Modificar cuenta", icon=ft.Icons.EDIT, on_click=modificar_cuenta),
            ft.PopupMenuItem(text="🔓 Cerrar sesión", icon=ft.Icons.LOGOUT, on_click=cerrar_sesion)
        ]
    )

    card = ft.Container(
        content=ft.Column([
            ft.Text(f"👨‍🎓 Bienvenido, {datos.get('nombre_alumno', '')}", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Aquí verás tus viajes asignados."),
            ft.Divider(),
            ft.Text("☰ Opciones", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            menu_usuario,
            ft.ElevatedButton(
                "Volver al menú",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: volver_callback(page)
            )
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        alignment=ft.alignment.center,
        width=500
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[card],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            expand=True
        )
    )