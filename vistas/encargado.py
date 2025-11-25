import flet as ft
from vistas.componentes import card, titulo

def encargado_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()

    # --- Helpers de UI ---
    def mostrar_mensaje(texto: str):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    def accion(tipo: str, operacion: str, registro_id=None):
        msg = f"{operacion} en {tipo}"
        if registro_id is not None:
            msg += f" (ID: {registro_id})"
        mostrar_mensaje(msg)

    # --- Contenedor donde montamos las tablas (se reemplaza dinámicamente) ---
    tabla_container = ft.Container(expand=True)

    # --- Datos simulados: reemplázalos por tus DAO al integrarlo ---
    data = {
        "Estudiantes": {
            "atributos": ["id", "nombre", "correo", "carrera", "semestre", "matricula"],
            "registros": [
                {"id": 1, "nombre": "Juan Pérez", "correo": "juan@correo.com", "carrera": "Sistemas", "semestre": "7", "matricula": "UAEM-2020-001"},
                {"id": 2, "nombre": "Ana López", "correo": "ana@correo.com", "carrera": "Administración", "semestre": "5", "matricula": "UAEM-2021-023"},
            ]
        },
        "Taxistas": {
            "atributos": ["id", "nombre", "placa", "telefono", "id_unidad", "estado_unidad"],
            "registros": [
                {"id": 10, "nombre": "Carlos Ruiz", "placa": "ABC123", "telefono": "555-1234", "id_unidad": "U-12", "estado_unidad": "Activa"},
                {"id": 11, "nombre": "Luis Gómez", "placa": "XYZ789", "telefono": "555-5678", "id_unidad": "U-22", "estado_unidad": "Mantenimiento"},
            ]
        },
        "Encargados": {
            "atributos": ["id", "nombre", "usuario", "rol", "correo"],
            "registros": [
                {"id": 100, "nombre": "Marta Díaz", "usuario": "marta", "rol": "Admin", "correo": "marta@uaem.mx"},
                {"id": 101, "nombre": "Pedro Sánchez", "usuario": "pedro", "rol": "Supervisor", "correo": "pedro@uaem.mx"},
            ]
        }
    }

    # --- Renderizado de tabla dinámica con scroll y acciones por fila ---
    def render_tabla(tipo: str):
        info = data.get(tipo, {"atributos": [], "registros": []})
        atributos = info["atributos"]
        registros = info["registros"]

        # Columnas (atributos + Acciones)
        columnas = [ft.DataColumn(ft.Text(attr)) for attr in atributos] + [ft.DataColumn(ft.Text("Acciones"))]

        # Filas
        filas = []
        for r in registros:
            celdas = [ft.DataCell(ft.Text(str(r.get(attr, "")))) for attr in atributos]
            acciones = ft.Row([
                ft.IconButton(icon=ft.Icons.EDIT, tooltip="Actualizar",
                              on_click=lambda e, rid=r["id"]: accion(tipo, "Actualizar", rid)),
                ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar",
                              on_click=lambda e, rid=r["id"]: accion(tipo, "Eliminar", rid)),
            ], spacing=6)
            celdas.append(ft.DataCell(acciones))
            filas.append(ft.DataRow(cells=celdas))

        # ✅ Corrección aquí
        tabla = ft.DataTable(columns=columnas, rows=filas)

        tabla_scroll = ft.Container(
            content=tabla,
            bgcolor=ft.Colors.WHITE,
            padding=12,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8),
        )

        # Limpiar y montar nueva tabla
        tabla_container.content = ft.Column([
            titulo(f"📋 Registros de {tipo}", 24),
            ft.Container(
                content=ft.Column([tabla_scroll], scroll=ft.ScrollMode.AUTO),
                expand=True
            ),
            ft.ElevatedButton(
                "🔙 Volver", icon=ft.Icons.ARROW_BACK,
                bgcolor=ft.Colors.GREY_200, color=ft.Colors.GREY_800,
                on_click=lambda e: encargado_view(page, datos, volver_callback)
            )
        ], spacing=16)
        page.update()

    # --- Tarjeta CRUD reutilizable ---
    def tarjeta_crud(titulo_texto: str, color, icono, tipo: str):
        return card(
            ft.Column([
                ft.Row([
                    ft.Icon(icono, color=color, size=26),
                    ft.Text(titulo_texto, size=22, weight=ft.FontWeight.BOLD, color=color)
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton(
                        "📋 Mostrar", icon=ft.Icons.LIST,
                        bgcolor=ft.Colors.GREEN_100, color=ft.Colors.GREEN_900,
                        on_click=lambda e: render_tabla(tipo)
                    ),
                    ft.ElevatedButton(
                        "➕ Crear", icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_900,
                        on_click=lambda e: accion(tipo, "Crear")
                    )
                ], spacing=10)
            ], spacing=12),
            width=420
        )

    # --- Menú hamburguesa ---
    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[
            ft.PopupMenuItem(text="🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ]
    )

    # --- Tarjetas por tipo ---
    estudiantes_card = tarjeta_crud("👨‍🎓 Estudiantes", ft.Colors.BLUE_800, ft.Icons.SCHOOL, "Estudiantes")
    taxistas_card = tarjeta_crud("🚖 Taxistas", ft.Colors.GREEN_800, ft.Icons.DIRECTIONS_CAR, "Taxistas")
    encargados_card = tarjeta_crud("🧑‍💼 Encargados", ft.Colors.ORANGE_800, ft.Icons.ADMIN_PANEL_SETTINGS, "Encargados")

    # --- Layout principal ---
    page.add(
        ft.Column([
            ft.Row([
                titulo("🧑‍💼 Panel del Encargado", 26),
                ft.Container(content=menu, alignment=ft.alignment.center_right)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            card(ft.Column([
                ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
                ft.Text(f"📧 Usuario: {datos.get('usuario', '')}", size=18),
                ft.Text(f"🔐 Rol: {datos.get('rol', '')}", size=18),
                ft.Text(f"🆔 ID: {datos.get('id_usuario', '')}", size=18)
            ], spacing=8), width=400, color=ft.Colors.BLUE_50),

            titulo("📂 Administración de usuarios", 22, ft.Colors.BLUE_800),

            ft.Row([estudiantes_card, taxistas_card, encargados_card],
                   wrap=True, alignment=ft.MainAxisAlignment.CENTER),

            tabla_container
        ], spacing=20, scroll=ft.ScrollMode.AUTO)
    )