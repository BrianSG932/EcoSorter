import flet as ft
from login import AuthManager

class SettingsScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.current_user = "admin"
        self.setup_ui()

    def setup_ui(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Configuraciones"

        self.file_picker = ft.FilePicker(on_result=self.on_photo_picked)
        self.page.overlay.append(self.file_picker)

        self.user_photo = ft.Container(
            content=ft.Image(
                src=self.auth_manager.users.get(self.current_user, {}).get("photo", "/default_avatar.png"),
                width=100,
                height=100,
                fit=ft.ImageFit.COVER
            ),
            width=120,
            height=120,
            border_radius=60,
            border=ft.border.all(2, ft.colors.BLUE_600),
            alignment=ft.alignment.center
        )

        self.username_field = ft.TextField(
            label="Nuevo Nombre de Usuario",
            width=300,
            value=self.auth_manager.users.get(self.current_user, {}).get("username", "")
        )
        self.password_field = ft.TextField(label="Nueva Contraseña", password=True, width=300)
        self.message = ft.Text(value="", color=ft.colors.RED, visible=False)

        self.language_dropdown = ft.Dropdown(
            label="Idioma",
            options=[
                ft.dropdown.Option("es", "Español"),
                ft.dropdown.Option("en", "Inglés"),
                ft.dropdown.Option("fr", "Francés")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("language", "es"),
            width=300
        )
        self.theme_dropdown = ft.Dropdown(
            label="Tema",
            options=[
                ft.dropdown.Option("light", "Claro"),
                ft.dropdown.Option("dark", "Oscuro")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("theme", "light"),
            width=300,
            on_change=self.change_theme
        )
        self.units_dropdown = ft.Dropdown(
            label="Unidades",
            options=[
                ft.dropdown.Option("metric", "Métrico (kg, m)"),
                ft.dropdown.Option("imperial", "Imperial (lb, ft)")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("units", "metric"),
            width=300
        )
        self.notifications_dropdown = ft.Dropdown(
            label="Frecuencia de Notificaciones",
            options=[
                ft.dropdown.Option("daily", "Diarias"),
                ft.dropdown.Option("weekly", "Semanales"),
                ft.dropdown.Option("off", "Desactivadas")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("notifications", "daily"),
            width=300
        )
        self.location_field = ft.TextField(
            label="Ubicación Predeterminada (Ciudad)",
            width=300,
            value=self.auth_manager.users.get(self.current_user, {}).get("location", "")
        )

        self.map_type_dropdown = ft.Dropdown(
            label="Modo de Mapa",
            options=[
                ft.dropdown.Option("roadmap", "Estándar"),
                ft.dropdown.Option("satellite", "Satélite"),
                ft.dropdown.Option("terrain", "Terreno")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("map_prefs", {}).get("map_type", "roadmap"),
            width=300
        )
        self.search_radius_dropdown = ft.Dropdown(
            label="Radio de Búsqueda",
            options=[
                ft.dropdown.Option("5000", "5 km"),
                ft.dropdown.Option("10000", "10 km"),
                ft.dropdown.Option("20000", "20 km")
            ],
            value=str(self.auth_manager.users.get(self.current_user, {}).get("map_prefs", {}).get("search_radius", 5000)),
            width=300
        )
        self.visible_residues_checklist = ft.Column(
            [
                ft.Checkbox(
                    label=residue,
                    value=residue in self.auth_manager.users.get(self.current_user, {}).get("map_prefs", {}).get("visible_residues", ["all"]),
                    data=residue
                ) for residue in ["Plástico", "Papel", "Vidrio", "Orgánico", "Metal", "Pilas", "Electrónicos"]
            ]
        )

        self.upload_photo_button = ft.ElevatedButton(
            text="Cambiar Foto",
            icon=ft.icons.UPLOAD,
            on_click=lambda e: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "png", "jpeg"]),
            width=300,
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE
        )
        self.remove_photo_button = ft.ElevatedButton(
            text="Eliminar Foto",
            icon=ft.icons.DELETE,
            on_click=self.remove_photo,
            width=300,
            bgcolor=ft.colors.RED_700,
            color=ft.colors.WHITE
        )
        self.update_account_button = ft.ElevatedButton(
            text="Guardar Cambios",
            icon=ft.icons.SAVE,
            on_click=self.update_account,
            width=300,
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE
        )
        self.logout_button = ft.ElevatedButton(
            text="Cerrar Sesión",
            icon=ft.icons.LOGOUT,
            on_click=lambda e: self.navigator.navigate("login"),
            width=300,
            bgcolor=ft.colors.RED_600,
            color=ft.Colors.WHITE
        )

        # Back arrow with no background
        back_arrow = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.BLACK,
            style=ft.ButtonStyle(bgcolor=None),
            on_click=lambda e: self.navigator.navigate("home"),
            tooltip="Volver al Inicio",
            icon_size=30,
            width=40,
            height=40
        )

        # Main content column
        main_content = ft.Column(
            [
                ft.Text("Configuraciones", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.Text("Personaliza tu experiencia y gestiona tu cuenta.", size=16, color=ft.colors.BLACK54),
                ft.Divider(),
                ft.Text("Perfil", size=20, weight=ft.FontWeight.BOLD),
                self.user_photo,
                ft.Row(
                    [self.upload_photo_button, self.remove_photo_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                self.username_field,
                self.password_field,
                ft.Divider(),
                ft.Text("Preferencias", size=20, weight=ft.FontWeight.BOLD),
                self.language_dropdown,
                self.theme_dropdown,
                self.units_dropdown,
                ft.Divider(),
                ft.Text("Notificaciones", size=20, weight=ft.FontWeight.BOLD),
                self.notifications_dropdown,
                ft.Divider(),
                ft.Text("Mapa", size=20, weight=ft.FontWeight.BOLD),
                self.location_field,
                self.map_type_dropdown,
                self.search_radius_dropdown,
                ft.Text("Residuos Visibles en el Mapa", size=16, weight=ft.FontWeight.BOLD),
                self.visible_residues_checklist,
                self.message,
                ft.Row(
                    [self.update_account_button, self.logout_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    wrap=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Use Stack to position the back arrow in the top-left corner
        self.page.add(
            ft.Container(
                content=ft.Stack(
                    [
                        main_content,
                        ft.Container(
                            content=back_arrow,
                            alignment=ft.alignment.top_left,
                            padding=ft.padding.only(left=10, top=10)
                        )
                    ],
                    expand=True
                ),
                padding=20,
                bgcolor=ft.colors.GREY_100,
                border_radius=10
            )
        )
        self.page.update()

    def on_photo_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            photo_path = e.files[0].path
            self.user_photo.content.src = f"/{photo_path}"
            self.auth_manager.users[self.current_user]["photo"] = f"/{photo_path}"
            self.message.value = "Foto de perfil actualizada."
            self.message.color = ft.colors.GREEN
            self.message.visible = True
        else:
            self.message.value = "No se seleccionó una imagen válida (JPG o PNG)."
            self.message.color = ft.colors.RED
            self.message.visible = True
        self.page.update()

    def remove_photo(self, e):
        self.user_photo.content.src = "/default_avatar.png"
        self.auth_manager.users[self.current_user]["photo"] = "/default_avatar.png"
        self.message.value = "Foto de perfil eliminada."
        self.message.color = ft.colors.GREEN
        self.message.visible = True
        self.page.update()

    def update_account(self, e):
        username = self.username_field.value
        password = self.password_field.value
        language = self.language_dropdown.value
        theme = self.theme_dropdown.value
        units = self.units_dropdown.value
        notifications = self.notifications_dropdown.value
        location = self.location_field.value
        map_type = self.map_type_dropdown.value
        search_radius = int(self.search_radius_dropdown.value)
        visible_residues = [cb.data for cb in self.visible_residues_checklist.controls if cb.value]
        if not visible_residues:
            visible_residues = ["all"]
        success = True
        message = []

        if username and username != self.current_user:
            if username in self.auth_manager.users:
                success = False
                message.append("El nombre de usuario ya existe.")
            else:
                self.auth_manager.users[username] = self.auth_manager.users.pop(self.current_user)
                self.current_user = username
                message.append("Nombre de usuario actualizado.")

        if password:
            if len(password) < 4:
                success = False
                message.append("La contraseña debe tener al menos 4 caracteres.")
            else:
                self.auth_manager.users[self.current_user]["password"] = password
                message.append("Contraseña actualizada.")

        self.auth_manager.users[self.current_user].update({
            "language": language,
            "theme": theme,
            "units": units,
            "notifications": notifications,
            "location": location,
            "map_prefs": {
                "map_type": map_type,
                "search_radius": search_radius,
                "visible_residues": visible_residues
            },
            "recycling_stats": self.auth_manager.users.get(self.current_user, {}).get("recycling_stats", {
                "Plástico": 0, "Papel": 0, "Vidrio": 0, "Orgánico": 0, "Metal": 0, "Pilas": 0, "Electrónicos": 0
            })
        })
        message.append("Preferencias guardadas.")

        if not message:
            success = False
            message.append("No se realizaron cambios.")

        self.message.value = " ".join(message)
        self.message.color = ft.colors.GREEN if success else ft.colors.RED
        self.message.visible = True
        self.page.update()

    def change_theme(self, e):
        theme = self.theme_dropdown.value
        self.page.theme_mode = ft.ThemeMode.LIGHT if theme == "light" else ft.ThemeMode.DARK
        self.auth_manager.users[self.current_user]["theme"] = theme
        self.page.update()