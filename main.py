import flet as ft
from datetime import date
from controlador.controlador_usuario import ControladorUsuario
from controlador.controlador_conductor import ControladorConductor
from controlador.controlador_viaje import ControladorViaje

controlador_usuario = ControladorUsuario()
controlador_conductor = ControladorConductor()
controlador_viaje = ControladorViaje()

def main(page: ft.Page):
    page.title = "Agenda de Taxis"
    page.theme_mode = "light"

    def menu_principal():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("🚕 Bienvenido", size=30, weight="bold"),
                    ft.Text("Selecciona una opción:", size=20),
                    ft.ElevatedButton("🔐 Iniciar sesión", on_click=lambda e: iniciar_sesion()),
                    ft.ElevatedButton("📝 Crear cuenta", on_click=lambda e: crear_cuenta())
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True,
                padding=20
            )
        )

    def crear_cuenta():
        page.clean()

        nombre_input = ft.TextField(label="Nombre completo", prefix_icon=ft.icons.PERSON)
        usuario_input = ft.TextField(label="Usuario", prefix_icon=ft.icons.ACCOUNT_BOX)
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK)

        fecha_nacimiento = ft.TextField(label="Fecha de nacimiento", read_only=True, prefix_icon=ft.icons.CALENDAR_MONTH)
        picker = ft.DatePicker(
            on_change=lambda e: actualizar_fecha(e.data),
            first_date=date(1950, 1, 1),
            last_date=date(2025, 12, 31)
        )
        page.overlay.append(picker)

        def actualizar_fecha(valor):
            fecha_nacimiento.value = str(valor)
            fecha_nacimiento.update()
            page.update()

        def abrir_calendario():
            picker.open = True
            page.update()

        correo_input = ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL)
        grupo_input = ft.TextField(label="Grupo")
        cuenta_input = ft.TextField(label="Número de cuenta")
        sexo_dropdown = ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Femenino"),
                ft.dropdown.Option("Otro")
            ]
        )
        carrera_input = ft.TextField(label="Carrera universitaria")
        mensaje = ft.Text("", color="green")

        def registrar(e):
            if not fecha_nacimiento.value.strip():
                mensaje.value = "❌ Debes seleccionar una fecha de nacimiento"
                page.update()
                return
            try:
                datos = {
                    "nombre_alumno": nombre_input.value.strip(),
                    "usuario": usuario_input.value.strip(),
                    "password": pass_input.value.strip(),
                    "rol": "alumno",
                    "año_nacimiento": fecha_nacimiento.value.strip(),
                    "correo": correo_input.value.strip(),
                    "grupo": grupo_input.value.strip(),
                    "numero_cuenta": cuenta_input.value.strip(),
                    "sexo": sexo_dropdown.value,
                    "carrera": carrera_input.value.strip()
                }
                controlador_usuario.crear_usuario(datos)
                mensaje.value = "✅ Cuenta creada correctamente"
                page.snack_bar = ft.SnackBar(ft.Text("Cuenta registrada"))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                mensaje.value = f"❌ Error al registrar: {ex}"
                page.update()

        card = ft.Container(
            content=ft.Column([
                ft.Text("📝 Crear cuenta", size=28, weight="bold"),
                nombre_input,
                usuario_input,
                pass_input,
                fecha_nacimiento,
                ft.ElevatedButton("📅 Seleccionar fecha", on_click=lambda e: abrir_calendario()),
                correo_input,
                grupo_input,
                cuenta_input,
                sexo_dropdown,
                carrera_input,
                mensaje,
                ft.Row([
                    ft.ElevatedButton("Registrar", style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE), expand=True, on_click=registrar),
                    ft.ElevatedButton("Volver", style=ft.ButtonStyle(bgcolor=ft.colors.GREY_300), expand=True, on_click=lambda e: menu_principal())
                ], spacing=10)
            ], spacing=15, horizontal_alignment="center"),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.GREY_400, offset=ft.Offset(0, 4)),
            alignment=ft.alignment.center,
            width=500
        )

        page.add(ft.Container(content=card, alignment=ft.alignment.center, expand=True))

    def iniciar_sesion():
        page.clean()
        usuario_input = ft.TextField(label="Usuario", prefix_icon=ft.icons.ACCOUNT_BOX)
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK)
        mensaje = ft.Text("", color="red")

        def verificar(e):
            u = usuario_input.value.strip()
            p = pass_input.value.strip()
            datos = controlador_usuario.obtener_usuario_por_credenciales(u, p)
            if datos:
                rol = datos["rol"]
                nombre = datos["nombre_alumno"]
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Bienvenido {nombre} ({rol})"))
                page.snack_bar.open = True
                page.update()
                if rol == "alumno":
                    alumno_view(nombre)
                elif rol == "taxista":
                    taxista_view(nombre)
                elif rol == "encargado":
                    encargado_view(nombre)
            else:
                mensaje.value = "❌ Usuario o contraseña incorrectos"
                page.update()

        login_card = ft.Container(
            content=ft.Column([
                ft.Text("🔐 Iniciar sesión", size=28, weight="bold"),
                usuario_input,
                pass_input,
                mensaje,
                ft.Row([
                    ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE), expand=True, on_click=verificar),
                    ft.ElevatedButton("Volver", style=ft.ButtonStyle(bgcolor=ft.colors.GREY_300), expand=True, on_click=lambda e: menu_principal())
                ], spacing=10)
            ], spacing=15, horizontal_alignment="center"),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.GREY_400, offset=ft.Offset(0, 4)),
            alignment=ft.alignment.center,
            width=400
        )

        page.add(ft.Container(content=login_card, alignment=ft.alignment.center, expand=True))

    def alumno_view(nombre):
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"👨‍🎓 Bienvenido, {nombre}", size=25, weight="bold"),
                ft.Text("Aquí verás tus viajes asignados."),
                ft.ElevatedButton("🔙 Cerrar sesión", on_click=lambda e: menu_principal())
            ], alignment="center", spacing=10)
        )

    def taxista_view(nombre):
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"🚖 Panel del Taxista: {nombre}", size=25, weight="bold"),
                ft.Text("Tus viajes asignados aparecerán aquí."),
                ft.ElevatedButton("🔙 Cerrar sesión", on_click=lambda e: menu_principal())
            ], alignment="center", spacing=10)
        )

    def encargado_view(nombre):
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"🧑‍💼 Panel del Encargado: {nombre}", size=25, weight="bold"),
                ft.Text("Aquí puedes administrar taxis y ver estadísticas."),
                ft.ElevatedButton("🔙 Cerrar sesión", on_click=lambda e: menu_principal())
            ], alignment="center", spacing=10)
        )

    menu_principal()

ft.app(target=main)