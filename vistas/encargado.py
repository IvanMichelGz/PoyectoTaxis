import flet as ft

def encargado_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()

    # ---------- Menú hamburguesa ----------
    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[
            ft.PopupMenuItem(text="🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))
        ]
    )

    # ---------- Encabezado centrado ----------
    header = ft.Row([
        ft.Text("🧑‍💼 Panel del Encargado", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # ---------- Recuadro de información del encargado ----------
    info_card = ft.Container(
        content=ft.Column([
            ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
            ft.Text(f"📧 Usuario: {datos.get('usuario', '')}", size=18),
            ft.Text(f"🔐 Rol: {datos.get('rol', '')}", size=18),
            ft.Text(f"🆔 ID: {datos.get('id_usuario', '')}", size=18)
        ], spacing=8),
        bgcolor=ft.Colors.BLUE_50,
        padding=25,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=400,
        margin=10
    )

    # ---------- Función para mostrar registros con botones extra ----------
    def mostrar_registros(tipo: str, registros: list):
        lista = ft.Column(spacing=8)
        for i, r in enumerate(registros):
            lista.controls.append(ft.Text(f"{tipo} {i+1}: {r}", size=16))
        # Botones al final
        lista.controls.append(
            ft.Row([
                ft.ElevatedButton("✏️ Actualizar", icon=ft.Icons.EDIT,
                                  bgcolor=ft.Colors.YELLOW_100, color=ft.Colors.YELLOW_900,
                                  on_click=lambda e: accion(tipo, "Actualizar")),
                ft.ElevatedButton("🗑️ Eliminar", icon=ft.Icons.DELETE,
                                  bgcolor=ft.Colors.RED_100, color=ft.Colors.RED_900,
                                  on_click=lambda e: accion(tipo, "Eliminar")),
            ], spacing=10)
        )
        page.add(lista)
        page.update()

    # ---------- Acciones simuladas ----------
    def accion(tipo, operacion):
        page.snack_bar = ft.SnackBar(ft.Text(f"{operacion} en {tipo}"))
        page.snack_bar.open = True
        page.update()

    # ---------- Función para generar tarjetas CRUD ----------
    def tarjeta_crud(titulo, color, icono, tipo):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icono, color=color, size=26),
                    ft.Text(titulo, size=22, weight=ft.FontWeight.BOLD, color=color)
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton("➕ Crear", icon=ft.Icons.ADD,
                                      bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_900,
                                      on_click=lambda e: accion(tipo, "Crear")),
                    ft.ElevatedButton("📋 Mostrar", icon=ft.Icons.LIST,
                                      bgcolor=ft.Colors.GREEN_100, color=ft.Colors.GREEN_900,
                                      on_click=lambda e: mostrar_registros(tipo, ["Registro A", "Registro B", "Registro C"]))
                ], spacing=10)
            ], spacing=12),
            bgcolor=ft.Colors.WHITE,
            padding=25,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
            width=420,
            margin=10
        )

    # ---------- Tarjetas por categoría ----------
    estudiantes_card = tarjeta_crud("👨‍🎓 Estudiantes", ft.Colors.BLUE_800, ft.Icons.SCHOOL, "Estudiantes")
    taxistas_card = tarjeta_crud("🚖 Taxistas", ft.Colors.GREEN_800, ft.Icons.DIRECTIONS_CAR, "Taxistas")
    encargados_card = tarjeta_crud("🧑‍💼 Encargados", ft.Colors.ORANGE_800, ft.Icons.ADMIN_PANEL_SETTINGS, "Encargados")

    # ---------- Layout principal ----------
    page.add(
        ft.Column([
            header,
            ft.Container(content=menu, alignment=ft.alignment.center_right),
            info_card,
            ft.Text("📂 Administración de usuarios", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Row([estudiantes_card, taxistas_card, encargados_card], wrap=True, alignment=ft.MainAxisAlignment.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO)
    )