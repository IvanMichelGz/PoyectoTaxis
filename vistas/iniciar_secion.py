import flet as ft
from controlador.controlador_usuario import ControladorUsuario

controlador_usuario = ControladorUsuario()

def iniciar_sesion(page: ft.Page, menu_principal, crear_cuenta, navegar_callback):
    page.clean()

    # Inicializa SnackBar con setattr para evitar error del editor
    setattr(page, "snack_bar", ft.SnackBar(content=ft.Text("")))

    def mostrar_snack(texto):
        try:
            # Ruta A: usar propiedad page.snack_bar
            page.snack_bar.content = ft.Text(texto)
            page.snack_bar.open = True
            page.update()
        except Exception:
            # Ruta B: fallback oficial de Flet
            page.show_snack_bar(ft.SnackBar(content=ft.Text(texto)))

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

        if not u or not p:
            mensaje.value = "❌ Debes ingresar usuario y contraseña"
            page.update()
            return

        datos = controlador_usuario.obtener_usuario_por_credenciales(u, p)
        if datos:
            mensaje.value = "✅ Inicio de sesión con éxito"
            page.update()
            navegar_callback(page, datos, menu_principal, crear_cuenta)
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    def recuperar_contraseña(e):
        correo_input = ft.TextField(label="Correo registrado", width=300)

        def enviar_recuperacion(ev):
            correo = correo_input.value.strip()
            if not correo:
                mostrar_snack("❌ Ingresa un correo")
                return

            usuario = controlador_usuario.dao.buscar_por_correo(correo)
            if usuario:
                mostrar_snack("📧 Se enviaron instrucciones de recuperación (simulado)")
            else:
                mostrar_snack("❌ Correo no encontrado")

            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Recuperar contraseña"),
            content=ft.Column([
                ft.Text("Ingresa tu correo para recuperar tu contraseña:"),
                correo_input
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev: setattr(page.dialog, "open", False)),
                ft.TextButton("Enviar", on_click=enviar_recuperacion)
            ]
        )
        page.dialog.open = True
        page.update()

    login_card = ft.Container(
        content=ft.Column([
            ft.Text("🔐 Iniciar sesión", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            usuario_input,
            pass_input,
            mensaje,
            ft.Row([
                ft.ElevatedButton("Ingresar", icon=ft.Icons.LOGIN, on_click=verificar, expand=True),
                ft.ElevatedButton(
                    "Volver",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: menu_principal(page, iniciar_sesion, crear_cuenta, navegar_callback),
                    expand=True
                )
            ], spacing=10),
            ft.Divider(),
            ft.ElevatedButton(
                "🔐 Recuperar contraseña",
                icon=ft.Icons.VPN_KEY,
                on_click=recuperar_contraseña,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_100,
                    color=ft.Colors.BLUE_900,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=10
                )
            )
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