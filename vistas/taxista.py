import flet as ft
from controlador.controlador_usuario import ControladorUsuario
from dao.viaje_dao import ViajeDAO


def taxista_view(page: ft.Page, datos: dict, volver_callback):
    page.clean()
    controlador = ControladorUsuario()
    viaje_dao = ViajeDAO()

    # ---------- Utilidades ----------
    def mostrar_mensaje(texto: str):
        page.snack_bar = ft.SnackBar(ft.Text(texto))
        page.snack_bar.open = True
        page.update()

    def limpiar_contenido():
        # Mantiene encabezado y tarjetas principales, pero limpia cualquier lista extra agregada
        # Usaremos un contenedor dedicado para contenido dinámico
        contenido_dinamico.controls.clear()
        page.update()

    # ---------- Modificar perfil ----------
    def modificar_perfil(e):
        page.clean()

        nombre_field = ft.TextField(label="👤 Nombre", value=datos.get("nombre_alumno", ""), width=340)
        correo_field = ft.TextField(label="📧 Correo", value=datos.get("correo", ""), width=340)
        telefono_field = ft.TextField(label="📞 Teléfono", value=datos.get("telefono", ""), width=340)
        placa_field = ft.TextField(label="🚗 Placa", value=datos.get("placa", ""), width=340)
        unidad_field = ft.TextField(label="🆔 Unidad", value=str(datos.get("id_unidad", "")), width=340)

        def guardar(ev):
            nuevos_datos = {
                "id_usuario": datos["id_usuario"],
                "nombre_alumno": nombre_field.value,
                "correo": correo_field.value,
                "telefono": telefono_field.value,
                "placa": placa_field.value,
                "id_unidad": unidad_field.value,
            }
            controlador.actualizar_usuario(nuevos_datos)
            mostrar_mensaje("✅ Perfil actualizado")
            taxista_view(page, nuevos_datos, volver_callback)

        page.add(
            ft.Column(
                [
                    ft.Text("✏️ Modificar perfil", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    nombre_field,
                    correo_field,
                    telefono_field,
                    placa_field,
                    unidad_field,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "💾 Guardar",
                                bgcolor=ft.Colors.BLUE_100,
                                color=ft.Colors.BLUE_900,
                                on_click=guardar,
                            ),
                            ft.ElevatedButton(
                                "⬅️ Volver",
                                bgcolor=ft.Colors.GREY_200,
                                color=ft.Colors.GREY_800,
                                on_click=lambda e: taxista_view(page, datos, volver_callback),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            )
        )

    # ---------- Viajes ----------
    def cambiar_estado(id_viaje, nuevo_estado):
        viaje_dao.actualizar_estado_viaje(id_viaje, nuevo_estado)
        mostrar_mensaje(f"🚖 Viaje {id_viaje} marcado como {nuevo_estado}")
        actualizar_viajes(None)

    def render_item_viaje(viaje: dict) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"📍 Destino: {viaje['destino']}", size=16, weight=ft.FontWeight.W_600),
                            ft.Text(f"🏷️ Estado: {viaje['estado']}", size=14, color=ft.Colors.BLUE_700),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "▶ Iniciar",
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=lambda e, id=viaje["id_viaje"]: cambiar_estado(id, "en curso"),
                            ),
                            ft.ElevatedButton(
                                "✅ Finalizar",
                                icon=ft.Icons.CHECK,
                                on_click=lambda e, id=viaje["id_viaje"]: cambiar_estado(id, "finalizado"),
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.BLUE_50,
            padding=12,
            border_radius=8,
        )

    def actualizar_viajes(e):
        limpiar_contenido()
        viajes = viaje_dao.obtener_viajes_por_taxista(datos["id_usuario"])
        if not viajes:
            contenido_dinamico.controls.append(ft.Text("No tienes viajes asignados", color=ft.Colors.GREY_700))
        else:
            contenido_dinamico.controls.append(
                ft.Column([render_item_viaje(v) for v in viajes], spacing=10)
            )
        page.update()

    # ---------- Ver mapa (diseño atractivo) ----------
    def tarjeta_base_taxi(nombre: str, ubicacion: str, horario: str, rating: str, url_maps: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                foreground_image_url=None,
                                bgcolor=ft.Colors.BLUE_200,
                                content=ft.Icon(ft.Icons.LOCAL_TAXI, color=ft.Colors.BLUE_900),
                                radius=18,
                            ),
                            ft.Text(nombre, size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED_400, size=16),
                            ft.Text(ubicacion, size=14),
                        ],
                        spacing=6,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.BLUE_400, size=16),
                            ft.Text(horario, size=14),
                        ],
                        spacing=6,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=16),
                            ft.Text(rating, size=14),
                        ],
                        spacing=6,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                "🌐 Abrir en Maps",
                                on_click=lambda e: page.launch_url(url_maps),
                            ),
                            ft.TextButton(
                                "⬅️ Volver",
                                on_click=lambda e: regresar_panel(),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=8,
            ),
            width=300,
            bgcolor=ft.Colors.WHITE,
            padding=16,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        )

    def ver_mapa(e):
        page.clean()
        titulo = ft.Text("🗺️ Bases de taxis cercanas", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
        grid = ft.Row(
            [
                tarjeta_base_taxi(
                    "Concepción Chico",
                    "San Felipe del Progreso, MEX",
                    "6:00 AM - 10:00 PM",
                    "⭐ 4.8",
                    "https://maps.google.com",
                ),
                tarjeta_base_taxi(
                    "Base Atlacomulco",
                    "Av. José María Morelos 102",
                    "24 horas",
                    "⭐ 5.0",
                    "https://maps.google.com",
                ),
                tarjeta_base_taxi(
                    "Tepetitlán - Tungareo",
                    "Cobertura regional",
                    "7:00 AM - 9:00 PM",
                    "⭐ 4.5",
                    "https://maps.google.com",
                ),
            ],
            wrap=True,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        page.add(
            ft.Column(
                [
                    titulo,
                    grid,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            )
        )

    def regresar_panel():
        taxista_view(page, datos, volver_callback)

    # ---------- Ver estadísticas ----------
    def ver_estadisticas(e):
        limpiar_contenido()
        viajes = viaje_dao.obtener_viajes_por_taxista(datos["id_usuario"])
        pendientes = sum(1 for v in viajes if v["estado"] == "pendiente")
        en_curso = sum(1 for v in viajes if v["estado"] == "en curso")
        finalizados = sum(1 for v in viajes if v["estado"] == "finalizado")

        contenido_dinamico.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("🟡 Pendientes", weight=ft.FontWeight.BOLD),
                                    ft.Text(str(pendientes), size=22, weight=ft.FontWeight.W_600),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.Colors.YELLOW_50,
                            padding=16,
                            border_radius=12,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("🔵 En curso", weight=ft.FontWeight.BOLD),
                                    ft.Text(str(en_curso), size=22, weight=ft.FontWeight.W_600),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=16,
                            border_radius=12,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("✅ Finalizados", weight=ft.FontWeight.BOLD),
                                    ft.Text(str(finalizados), size=22, weight=ft.FontWeight.W_600),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.Colors.GREEN_50,
                            padding=16,
                            border_radius=12,
                            expand=True,
                        ),
                    ],
                    spacing=12,
                ),
                padding=4,
            )
        )
        page.update()

    # ---------- Menú ----------
    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        items=[
            ft.PopupMenuItem(text="✏️ Modificar perfil", on_click=modificar_perfil),
            ft.PopupMenuItem(text="🔒 Cerrar sesión", on_click=lambda e: volver_callback(page)),
        ],
    )

    # ---------- Encabezado ----------
    header = ft.Row(
        [
            ft.Text("🚖 Panel del Taxista", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Container(content=menu, alignment=ft.alignment.center_right),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ---------- Tarjeta de datos ----------
    info_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"👤 {datos.get('nombre_alumno', '')}", size=18),
                ft.Text(f"📧 {datos.get('correo', '')}", size=18),
                ft.Text(f"📞 {datos.get('telefono', '')}", size=18),
                ft.Text(f"🚗 {datos.get('placa', '')}", size=18),
                ft.Text(f"🆔 Unidad {datos.get('id_unidad', '')}", size=18),
            ],
            spacing=8,
        ),
        bgcolor=ft.Colors.BLUE_50,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=380,
        margin=10,
    )

    # ---------- Tarjeta de viajes ----------
    viajes_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("📋 Tus viajes asignados", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.Text("Aquí aparecerán los viajes pendientes, en curso o finalizados."),
                ft.ElevatedButton("🔄 Actualizar lista", icon=ft.Icons.REFRESH, expand=True, on_click=actualizar_viajes),
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=380,
        margin=10,
    )

    # ---------- Tarjeta de opciones ----------
    opciones_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("⚙️ Opciones rápidas", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.Row(
                    [
                        ft.ElevatedButton("📍 Ver mapa", icon=ft.Icons.MAP, on_click=ver_mapa),
                        ft.ElevatedButton("📊 Estadísticas", icon=ft.Icons.BAR_CHART, on_click=ver_estadisticas),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400, offset=ft.Offset(0, 4)),
        width=380,
        margin=10,
    )

    # ---------- Contenido dinámico ----------
    contenido_dinamico = ft.Column(spacing=12)

    # ---------- Layout ----------
    page.add(
        ft.Column(
            [
                header,
                ft.Row([info_card, viajes_card, opciones_card], wrap=True, spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                contenido_dinamico,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )
    )