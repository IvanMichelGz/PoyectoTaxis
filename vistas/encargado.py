import flet as ft
from vistas.componentes import card, titulo
from dao.usuario_dao import UsuarioDAO
from dao.conductor_dao import ConductorDAO


def encargado_view(page: ft.Page, datos: dict, volver_callback):
    # Limpieza y configuración de scroll global
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    # DAOs
    usuario_dao = UsuarioDAO()
    conductor_dao = ConductorDAO()

    # Mensajes toast/snackbar
    def toast(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # Contenedor que se reemplaza con cada tabla/formulario
    tabla_container = ft.Container(expand=True)

    # ------------------ CRUD Usuarios (Estudiantes / Encargados) ------------------

    def crear_usuario_dialog(rol: str):
        nombre = ft.TextField(label="Nombre completo", autofocus=True)
        usuario = ft.TextField(label="Usuario")
        correo = ft.TextField(label="Correo")
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        grupo = ft.TextField(label="Grupo")
        carrera = ft.TextField(label="Carrera")
        telefono = ft.TextField(label="Teléfono")
        direccion = ft.TextField(label="Dirección")

        def guardar(e):
            try:
                datos = {
                    "nombre_alumno": nombre.value.strip(),
                    "usuario": usuario.value.strip(),
                    "password": password.value.strip(),
                    "rol": rol.lower(),
                    "año_nacimiento": None,
                    "correo": correo.value.strip(),
                    "grupo": grupo.value.strip(),
                    "numero_cuenta": None,
                    "sexo": None,
                    "carrera": carrera.value.strip(),
                    "placa": None,
                    "id_unidad": None,
                    "puesto": None,
                    "telefono": telefono.value.strip(),
                    "direccion": direccion.value.strip()
                }
                usuario_dao.insertar(datos)
                toast(f"{rol} creado correctamente")
                dlg.open = False
                page.update()
                render_tabla(rol)
            except Exception as ex:
                toast(f"Error al crear {rol}: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text(f"Crear nuevo {rol}"),
            content=ft.Column([
                nombre, usuario, password, correo, grupo, carrera, telefono, direccion
            ], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, "open", False)),
                ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def actualizar_usuario_dialog(registro: dict, rol: str):
        nombre = ft.TextField(label="Nombre", value=str(registro.get("nombre", "")), autofocus=True)
        correo = ft.TextField(label="Correo", value=str(registro.get("correo", "")))
        usuario = ft.TextField(label="Usuario", value=str(registro.get("usuario", "")))

        def guardar(e):
            try:
                n = nombre.value.strip()
                c = correo.value.strip()
                u = usuario.value.strip()
                if not n or not c or not u:
                    toast("Completa todos los campos")
                    return

                usuario_dao.actualizar(registro["id_usuario"], {
                    "nombre": n,
                    "correo": c,
                    "usuario": u,
                    "rol": rol.lower()
                })
                toast(f"{rol} {registro['id_usuario']} actualizado")
                dlg.open = False
                page.update()
                render_tabla(rol)
            except Exception as ex:
                toast(f"Error al actualizar {rol}: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text(f"Actualizar {rol} #{registro['id_usuario']}"),
            content=ft.Column([nombre, correo, usuario], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, "open", False)),
                ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def eliminar_usuario(id_usuario: int, rol: str):
        try:
            usuario_dao.eliminar(id_usuario)
            toast(f"{rol} {id_usuario} eliminado")
            render_tabla(rol)
        except Exception as ex:
            toast(f"Error al eliminar {rol}: {ex}")

    # ------------------ CRUD Conductores ------------------

    def crear_conductor_dialog():
        id_unidad = ft.TextField(label="ID Unidad", autofocus=True)
        placa = ft.TextField(label="Placa")
        nombre = ft.TextField(label="Nombre del conductor")

        def guardar(e):
            try:
                iu = id_unidad.value.strip()
                p = placa.value.strip()
                nc = nombre.value.strip()
                if not iu or not p or not nc:
                    toast("Completa todos los campos")
                    return

                conductor_dao.insert({"id_unidad": iu, "placa": p, "nombre_conductor": nc})
                toast("Conductor creado correctamente")
                dlg.open = False
                page.update()
                render_tabla("Conductores")
            except Exception as ex:
                toast(f"Error al crear conductor: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text("Crear conductor"),
            content=ft.Column([id_unidad, placa, nombre], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, "open", False)),
                ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def actualizar_conductor_dialog(registro: dict):
        id_unidad = ft.TextField(label="ID Unidad", value=str(registro.get("id_unidad", "")), autofocus=True)
        placa = ft.TextField(label="Placa", value=str(registro.get("placa", "")))
        nombre = ft.TextField(label="Nombre del conductor", value=str(registro.get("nombre_conductor", "")))

        def guardar(e):
            try:
                iu = id_unidad.value.strip()
                p = placa.value.strip()
                nc = nombre.value.strip()
                if not iu or not p or not nc:
                    toast("Completa todos los campos")
                    return

                q = "UPDATE Conductor SET id_unidad=?, placa=?, nombre_conductor=? WHERE id_conductor=?"
                conductor_dao.cursor.execute(q, (iu, p, nc, registro["id_conductor"]))
                conductor_dao.conn.commit()
                toast(f"Conductor {registro['id_conductor']} actualizado")
                dlg.open = False
                page.update()
                render_tabla("Conductores")
            except Exception as ex:
                toast(f"Error al actualizar conductor: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text(f"Actualizar conductor #{registro['id_conductor']}"),
            content=ft.Column([id_unidad, placa, nombre], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, "open", False)),
                ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def eliminar_conductor(id_conductor: int):
        try:
            conductor_dao.eliminar(id_conductor)
            toast(f"Conductor {id_conductor} eliminado")
            render_tabla("Conductores")
        except Exception as ex:
            toast(f"Error al eliminar conductor: {ex}")

    # ------------------ Render de tablas con scroll ------------------

    def render_tabla(tipo: str):
        # Cargar registros y definir columnas según tipo
        if tipo == "Estudiantes":
            registros = usuario_dao.obtener_por_rol("estudiante")
            atributos = ["id_usuario", "nombre_alumno", "correo", "usuario", "rol"]
        elif tipo == "Encargados":
            registros = usuario_dao.obtener_por_rol("encargado")
            atributos = ["id_usuario", "nombre", "correo", "usuario", "rol"]
        elif tipo == "Conductores":
            registros = conductor_dao.obtener_todos()
            atributos = ["id_conductor", "id_unidad", "placa", "nombre_conductor"]
        else:
            registros, atributos = [], []

        columnas = [ft.DataColumn(ft.Text(attr)) for attr in atributos] + [ft.DataColumn(ft.Text("Acciones"))]
        filas = []

        # Construcción de filas con captura segura de variables
        for r in registros:
            celdas = [ft.DataCell(ft.Text(str(r.get(attr, "")))) for attr in atributos]

            if tipo in ["Estudiantes", "Encargados"]:
                acciones = ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Actualizar",
                            on_click=lambda e, reg=r, rol=tipo: actualizar_usuario_dialog(reg, rol),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar",
                            on_click=lambda e, rid=r["id_usuario"], rol=tipo: eliminar_usuario(rid, rol),
                        ),
                    ],
                    spacing=6,
                )
            elif tipo == "Conductores":
                acciones = ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Actualizar",
                            on_click=lambda e, reg=r: actualizar_conductor_dialog(reg),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar",
                            on_click=lambda e, rid=r["id_conductor"]: eliminar_conductor(rid),
                        ),
                    ],
                    spacing=6,
                )
            else:
                acciones = ft.Row(controls=[], spacing=6)

            celdas.append(ft.DataCell(acciones))
            filas.append(ft.DataRow(cells=celdas))

        tabla = ft.DataTable(columns=columnas, rows=filas)

        # Montar tabla con encabezado y scroll
        tabla_container.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        titulo(f"📋 {tipo}", 24),
                        ft.FilledButton(
                            f"➕ Crear {tipo}",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: (
                                crear_usuario_dialog(tipo) if tipo in ["Estudiantes", "Encargados"] else crear_conductor_dialog()
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=12,
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8),
                ),
                ft.ElevatedButton(
                    "🔙 Volver",
                    icon=ft.Icons.ARROW_BACK,
                    bgcolor=ft.Colors.GREY_200,
                    color=ft.Colors.GREY_800,
                    on_click=lambda e: encargado_view(page, datos, volver_callback),
                ),
            ],
            spacing=16,
        )
        page.update()

    # ------------------ Tarjetas CRUD ------------------

    def tarjeta_crud(titulo_texto: str, color, icono, tipo: str):
        return card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icono, color=color, size=26),
                            ft.Text(titulo_texto, size=22, weight=ft.FontWeight.BOLD, color=color),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "📋 Mostrar",
                                icon=ft.Icons.LIST,
                                bgcolor=ft.Colors.GREEN_100,
                                color=ft.Colors.GREEN_900,
                                on_click=lambda e: render_tabla(tipo),
                            ),
                            ft.ElevatedButton(
                                "➕ Crear",
                                icon=ft.Icons.ADD,
                                bgcolor=ft.Colors.BLUE_100,
                                color=ft.Colors.BLUE_900,
                                on_click=lambda e: (
                                    crear_usuario_dialog(tipo) if tipo in ["Estudiantes", "Encargados"] else crear_conductor_dialog()
                                ),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=12,
            ),
            width=420,
        )

    # ------------------ Menú y layout principal ------------------

    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[ft.PopupMenuItem(text="🔙 Cerrar sesión", on_click=lambda e: volver_callback(page))],
    )

    estudiantes_card = tarjeta_crud("👨‍🎓 Estudiantes", ft.Colors.BLUE_800, ft.Icons.SCHOOL, "Estudiantes")
    conductores_card = tarjeta_crud("🚖 Conductores", ft.Colors.GREEN_800, ft.Icons.DIRECTIONS_CAR, "Conductores")
    encargados_card = tarjeta_crud("🧑‍💼 Encargados", ft.Colors.ORANGE_800, ft.Icons.ADMIN_PANEL_SETTINGS, "Encargados")

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        titulo("🧑‍💼 Panel del Encargado", 26),
                        ft.Container(content=menu, alignment=ft.alignment.center_right),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                card(
                    ft.Column(
                        controls=[
                            ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
                            ft.Text(f"📧 Usuario: {datos.get('usuario', '')}", size=18),
                            ft.Text(f"🔐 Rol: {datos.get('rol', '')}", size=18),
                            ft.Text(f"🆔 ID: {datos.get('id_usuario', '')}", size=18),
                        ],
                        spacing=8,
                    ),
                    width=400,
                    color=ft.Colors.BLUE_50,
                ),
                titulo("📂 Administración de usuarios", 22, ft.Colors.BLUE_800),
                ft.Row([estudiantes_card, conductores_card, encargados_card], wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                tabla_container,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )
    )