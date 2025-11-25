import flet as ft
from dao.usuario_dao import UsuarioDAO
from dao.conductor_dao import ConductorDAO
from vistas.componentes import titulo, card

def alumno_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    usuario_dao = UsuarioDAO()
    conductor_dao = ConductorDAO()

    def toast(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # ------------------ Acciones del alumno ------------------

    def solicitar_taxi():
        try:
            # Buscar un conductor disponible
            conductores = conductor_dao.obtener_todos()
            conductor_disp = next((c for c in conductores if c.get("estado") == "disponible"), None)

            if conductor_disp:
                # Asignar conductor al alumno
                usuario_dao.actualizar_usuario({
                    "id_usuario": datos["id_usuario"],
                    "nombre_alumno": datos["nombre_alumno"],
                    "correo": datos.get("correo"),
                    "grupo": datos.get("grupo"),
                    "carrera": datos.get("carrera"),
                    "telefono": datos.get("telefono"),
                    "direccion": datos.get("direccion"),
                    "estado": "pendiente",
                    "id_unidad": conductor_disp["id_unidad"],
                    "placa": conductor_disp["placa"]
                })
                # Cambiar estado del conductor a pendiente
                conductor_dao.actualizar_estado(conductor_disp["id_conductor"], "pendiente")

                toast(f"🚖 Taxi solicitado. Conductor asignado: {conductor_disp['nombre_conductor']}")
            else:
                toast("❌ No hay conductores disponibles en este momento")

            render_layout()
        except Exception as ex:
            toast(f"Error al solicitar taxi: {ex}")

    def esperar_taxi():
        try:
            usuario_dao.actualizar_usuario({
                "id_usuario": datos["id_usuario"],
                "nombre_alumno": datos["nombre_alumno"],
                "correo": datos.get("correo"),
                "grupo": datos.get("grupo"),
                "carrera": datos.get("carrera"),
                "telefono": datos.get("telefono"),
                "direccion": datos.get("direccion"),
                "estado": "esperando"
            })
            toast("⏳ Estás esperando un taxi")
            render_layout()
        except Exception as ex:
            toast(f"Error al marcar espera: {ex}")

    # ------------------ Cambiar estado de conductor ------------------

    def cambiar_estado_conductor(id_conductor, nuevo_estado):
        try:
            conductor_dao.actualizar_estado(id_conductor, nuevo_estado)
            toast(f"Estado del conductor {id_conductor} cambiado a {nuevo_estado}")
            render_layout()
        except Exception as ex:
            toast(f"Error al cambiar estado: {ex}")

    # ------------------ Tabla de conductores ------------------

    def render_conductores():
        registros = conductor_dao.obtener_todos()
        atributos = ["id_conductor", "id_unidad", "placa", "nombre_conductor", "estado"]

        columnas = [ft.DataColumn(ft.Text(attr)) for attr in atributos] + [ft.DataColumn(ft.Text("Acciones"))]
        filas = []

        for r in registros:
            celdas = [ft.DataCell(ft.Text(str(r.get(attr, "")))) for attr in atributos]

            estado = r.get("estado", "disponible").lower()
            if estado == "disponible":
                acciones = ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.LOCAL_TAXI,
                        tooltip="Solicitar taxi",
                        on_click=lambda e, rid=r["id_conductor"]: cambiar_estado_conductor(rid, "pendiente")
                    )
                ])
            elif estado == "pendiente":
                acciones = ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.HOURGLASS_BOTTOM,
                        tooltip="Esperar taxi",
                        on_click=lambda e, rid=r["id_conductor"]: cambiar_estado_conductor(rid, "ocupado")
                    )
                ])
            elif estado == "ocupado":
                acciones = ft.Row([
                    ft.Text("🚖 En servicio", size=14, color=ft.Colors.GREY)
                ])
            else:
                acciones = ft.Row([
                    ft.Text(f"Estado: {estado}", size=14, color=ft.Colors.GREY)
                ])

            celdas.append(ft.DataCell(acciones))
            filas.append(ft.DataRow(cells=celdas))

        tabla = ft.DataTable(columns=columnas, rows=filas)

        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo("🚖 Conductores disponibles", 22, ft.Colors.GREEN_800),
                    ft.Container(
                        content=tabla,
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        padding=12,
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=8),
                    ),
                ],
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )

    # ------------------ Layout principal ------------------

    def render_layout():
        page.clean()

        estado = datos.get("estado", "disponible")
        if estado == "disponible":
            botones = [
                ft.FilledButton("🚖 Solicitar taxi", icon=ft.Icons.LOCAL_TAXI, on_click=lambda e: solicitar_taxi())
            ]
        elif estado == "pendiente":
            botones = [
                ft.FilledButton("⏳ Esperar taxi", icon=ft.Icons.HOURGLASS_BOTTOM, on_click=lambda e: esperar_taxi())
            ]
        else:
            botones = [
                ft.Text(f"Estado actual: {estado}", size=16, color=ft.Colors.GREY)
            ]

        page.add(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            titulo("👨‍🎓 Panel del Alumno", 26),
                            ft.ElevatedButton("🔙 Volver", icon=ft.Icons.ARROW_BACK,
                                              on_click=lambda e: volver_callback(page))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # Información del alumno arriba
                    card(
                        ft.Column(
                            controls=[
                                ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
                                ft.Text(f"📧 Usuario: {datos.get('usuario', '')}", size=18),
                                ft.Text(f"🔐 Rol: {datos.get('rol', '')}", size=18),
                                ft.Text(f"🆔 ID: {datos.get('id_usuario', '')}", size=18),
                                ft.Row(botones, spacing=12),
                            ],
                            spacing=8,
                        ),
                        width=600,
                        color=ft.Colors.BLUE_50,
                    ),
                    # Tabla de conductores debajo
                    render_conductores()
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        page.update()

    render_layout()