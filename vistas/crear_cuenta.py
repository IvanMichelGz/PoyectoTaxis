import flet as ft
from datetime import date
from controlador.controlador_usuario import ControladorUsuario

controlador_usuario = ControladorUsuario()

def crear_cuenta(page: ft.Page, menu_principal, iniciar_sesion, navegar_callback):
    page.clean()

    def styled_input(label, icon=None, password=False):
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            password=password,
            can_reveal_password=password,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            border_color=ft.Colors.BLUE_200,
            label_style=ft.TextStyle(color=ft.Colors.BLUE_800)
        )

    nombre_input = styled_input("Nombre completo", ft.Icons.PERSON)
    usuario_input = styled_input("Usuario", ft.Icons.ACCOUNT_BOX)
    pass_input = styled_input("Contraseña", ft.Icons.LOCK, password=True)

    fecha_nacimiento = styled_input("Fecha de nacimiento", ft.Icons.CALENDAR_MONTH)
    fecha_nacimiento.read_only = True

    picker = ft.DatePicker(
        on_change=lambda e: actualizar_fecha(e.data),
        first_date=date(1950, 1, 1),
        last_date=date(2025, 12, 31)
    )
    page.overlay.append(picker)

    def actualizar_fecha(valor):
        fecha_nacimiento.value = str(valor)
        fecha_nacimiento.update()

    def abrir_calendario():
        picker.open = True
        page.update()

    correo_input = styled_input("Correo electrónico", ft.Icons.EMAIL)
    grupo_input = styled_input("Grupo")
    cuenta_input = styled_input("Número de cuenta")
    carrera_input = styled_input("Carrera universitaria")

    sexo_dropdown = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
            ft.dropdown.Option("Otro")
        ],
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.BLUE_50,
        border_color=ft.Colors.BLUE_200
    )

    mensaje = ft.Text("", color=ft.Colors.GREEN_600, size=14)

    def registrar(e):
        if not (fecha_nacimiento.value or "").strip():
            mensaje.value = "❌ Debes seleccionar una fecha de nacimiento"
            page.update()
            return

        if not all([nombre_input.value, usuario_input.value, pass_input.value, correo_input.value]):
            mensaje.value = "❌ Todos los campos obligatorios deben llenarse"
            page.update()
            return

        try:
            datos = {
                "nombre_alumno": (nombre_input.value or "").strip(),
                "usuario": (usuario_input.value or "").strip(),
                "password": (pass_input.value or "").strip(),
                "rol": "alumno",
                "año_nacimiento": (fecha_nacimiento.value or "").strip(),
                "correo": (correo_input.value or "").strip(),
                "grupo": (grupo_input.value or "").strip(),
                "numero_cuenta": (cuenta_input.value or "").strip(),
                "sexo": (sexo_dropdown.value),
                "carrera": (carrera_input.value or "").strip()
            }
            controlador_usuario.crear_usuario(datos)
            mensaje.value = "✅ Cuenta creada correctamente"
            page.update()
        except Exception as ex:
            mensaje.value = f"❌ Error al registrar: {ex}"
            page.update()

    formulario = ft.Container(
        content=ft.Column([
            ft.Text("📝 Crear cuenta", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            nombre_input,
            usuario_input,
            pass_input,
            fecha_nacimiento,
            ft.ElevatedButton(
                "📅 Seleccionar fecha",
                icon=ft.Icons.CALENDAR_MONTH,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_100,
                    color=ft.Colors.BLUE_900,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=10
                ),
                on_click=lambda e: abrir_calendario()
            ),
            correo_input,
            grupo_input,
            cuenta_input,
            sexo_dropdown,
            carrera_input,
            mensaje,
            ft.Row([
                ft.ElevatedButton(
                    "Registrar",
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=10
                    ),
                    expand=True,
                    on_click=registrar
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