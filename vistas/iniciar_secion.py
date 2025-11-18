import flet as ft
from controlador.controlador_usuario import ControladorUsuario

controlador_usuario = ControladorUsuario()

def iniciar_sesion(page: ft.Page, menu_principal, crear_cuenta, navegar_callback):
    page.clean()

    usuario_input = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.ACCOUNT_BOX,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.BLUE_50,
        border_color=ft.Colors.BLUE_200,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_800)
    )

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.BLUE_50,
        border_color=ft.Colors.BLUE_200,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_800)
    )

    mensaje = ft.Text("", color=ft.Colors.RED_600, size=14)

    def verificar(e):
        u = (usuario_input.value or "").strip()
        p = (pass_input.value or "").strip()
        datos = controlador_usuario.obtener_usuario_por_credenciales(u, p)
        if datos:
            mensaje.value = "✅ Inicio de sesión con éxito"
            page.update()
            navegar_callback(page, datos, menu_principal, crear_cuenta)  # ← pasamos page y callbacks
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    login_card = ft.Container(
        content=ft.Column([
            ft.Text("🔐 Iniciar sesión", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            usuario_input,
            pass_input,
            mensaje,
            ft.Row([
                ft.ElevatedButton(
                    "Ingresar",
                    icon=ft.Icons.LOGIN,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=10
                    ),
                    expand=True,
                    on_click=verificar
                ),
                ft.ElevatedButton(
                    "Volver",
                    icon=ft.Icons.ARROW_BACK,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_200,
                        color=ft.Colors.BLUE_900,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=10
                    ),
                    expand=True,
                    on_click=lambda e: menu_principal(page, iniciar_sesion, crear_cuenta, navegar_callback)
                )
            ], spacing=10)
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        alignment=ft.alignment.center,
        width=500
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[login_card],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            expand=True
        )
    )

def navegar_callback(page: ft.Page, datos_estudiante: dict, menu_principal, crear_cuenta):
    page.clean()

    nombre = datos_estudiante["nombre_alumno"]
    usuario = datos_estudiante["usuario"]
    correo = datos_estudiante["correo"]
    grupo = datos_estudiante["grupo"]
    cuenta = datos_estudiante["numero_cuenta"]
    carrera = datos_estudiante["carrera"]
    sexo = datos_estudiante["sexo"]

    def modificar_usuario(e):
        # Aquí puedes abrir un formulario editable con los datos actuales
        pass

    def eliminar_usuario(e):
        controlador_usuario.eliminar_por_id(datos_estudiante["id"])
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.SnackBar(ft.Text("✅ Cuenta eliminada")),
                bgcolor=ft.Colors.GREEN_100,
                open=True
            )
        )
        page.update()
        menu_principal(page, iniciar_sesion, crear_cuenta, navegar_callback)

    def cerrar_sesion(e):
        menu_principal(page, iniciar_sesion, crear_cuenta, navegar_callback)

    card = ft.Container(
        content=ft.Column([
            ft.Text(f"👤 Bienvenido, {nombre}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text(
                f"Usuario: {usuario}\nCorreo: {correo}\nGrupo: {grupo}\nCuenta: {cuenta}\nCarrera: {carrera}\nSexo: {sexo}",
                size=16
            ),
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton("Modificar", icon=ft.Icons.EDIT, on_click=modificar_usuario),
                ft.ElevatedButton("Eliminar", icon=ft.Icons.DELETE, on_click=eliminar_usuario),
                ft.ElevatedButton("Cerrar sesión", icon=ft.Icons.LOGOUT, on_click=cerrar_sesion)
            ], spacing=10)
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.WHITE,
        padding=30,
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