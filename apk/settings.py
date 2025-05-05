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

        # File picker for photo upload
        self.file_picker = ft.FilePicker(on_result=self.on_photo_picked)
        self.page.overlay.append(self.file_picker)

        # Back arrow
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

        title = ft.Text(
            "Configuraciones",
            size=34,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            font_family="Roboto"
        )

        # Edit Profile Section
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
            label="Nombre de usuario",
            width=300,
            value=self.auth_manager.users.get(self.current_user, {}).get("username", "")
        )
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            width=300
        )

        profile_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Editar Perfil")),
            content=ft.Column([
                self.user_photo,
                ft.Row([
                    ft.ElevatedButton(
                        text="Cambiar Foto",
                        icon=ft.icons.UPLOAD,
                        on_click=lambda e: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "png", "jpeg"]),
                        width=150,
                        bgcolor=ft.colors.ORANGE_600,
                        color=ft.colors.WHITE
                    ),
                    ft.ElevatedButton(
                        text="Eliminar Foto",
                        icon=ft.icons.DELETE,
                        on_click=self.remove_photo,
                        width=150,
                        bgcolor=ft.colors.RED_700,
                        color=ft.colors.WHITE
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                self.username_field,
                self.password_field,
                ft.ElevatedButton(
                    text="Guardar",
                    on_click=self.update_profile,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    width=150
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Language Section
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

        language_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Idioma")),
            content=ft.Column([
                self.language_dropdown,
                ft.ElevatedButton(
                    text="Aplicar",
                    on_click=self.change_language,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    width=150
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Theme Section
        self.theme_dropdown = ft.Dropdown(
            label="Tema",
            options=[
                ft.dropdown.Option("light", "Claro"),
                ft.dropdown.Option("dark", "Oscuro")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("theme", "light"),
            width=300
        )

        theme_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Tema")),
            content=ft.Column([
                self.theme_dropdown,
                ft.ElevatedButton(
                    text="Aplicar",
                    on_click=self.change_theme,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    width=150
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Notifications Section
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

        notifications_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Notificaciones")),
            content=ft.Column([
                self.notifications_dropdown,
                ft.ElevatedButton(
                    text="Guardar",
                    on_click=self.update_notifications,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    width=150
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Map Preferences Section
        self.units_dropdown = ft.Dropdown(
            label="Unidades",
            options=[
                ft.dropdown.Option("metric", "Métrico (kg, m)"),
                ft.dropdown.Option("imperial", "Imperial (lb, ft)")
            ],
            value=self.auth_manager.users.get(self.current_user, {}).get("units", "metric"),
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

        map_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Preferencias del Mapa")),
            content=ft.Column([
                self.units_dropdown,
                self.location_field,
                self.map_type_dropdown,
                self.search_radius_dropdown,
                ft.Text("Residuos Visibles en el Mapa", size=16, weight=ft.FontWeight.BOLD),
                self.visible_residues_checklist,
                ft.ElevatedButton(
                    text="Guardar",
                    on_click=self.update_map_prefs,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    width=150
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Logout Section
        logout_section = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("Cerrar Sesión")),
            content=ft.Column([
                ft.ElevatedButton(
                    text="Cerrar Sesión",
                    icon=ft.icons.LOGOUT,
                    on_click=lambda e: self.navigator.navigate("login"),
                    width=150,
                    bgcolor=ft.colors.RED_600,
                    color=ft.colors.WHITE
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

        # Expansion Panel List
        settings_list = ft.ExpansionPanelList(
            controls=[
                profile_section,
                language_section,
                theme_section,
                notifications_section,
                map_section,
                logout_section
            ],
            expand_icon_color=ft.colors.GREEN_600,
            elevation=2,
            divider_color=ft.colors.GREY_300,
            spacing=10
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([back_arrow, ft.Container(expand=True), title], alignment=ft.MainAxisAlignment.START),
                        settings_list
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30
                ),
                padding=30,
                bgcolor=ft.colors.GREY_100,
                expand=True
            )
        )
        self.page.update()

    def on_photo_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            photo_path = e.files[0].path
            self.user_photo.content.src = f"/{photo_path}"
            self.auth_manager.users[self.current_user]["photo"] = f"/{photo_path}"
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Foto de perfil actualizada correctamente"))
            self.page.snack_bar.open = True
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("No se seleccionó una imagen válida (JPG o PNG)"))
            self.page.snack_bar.open = True
        self.page.update()

    def remove_photo(self, e):
        self.user_photo.content.src = "/default_avatar.png"
        self.auth_manager.users[self.current_user]["photo"] = "/default_avatar.png"
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Foto de perfil eliminada"))
        self.page.snack_bar.open = True
        self.page.update()

    def update_profile(self, e):
        username = self.username_field.value
        password = self.password_field.value
        success = True
        message = []

        if username and username != self.current_user:
            if username in self.auth_manager.users:
                success = False
                message.append("El nombre de usuario ya existe")
            else:
                self.auth_manager.users[username] = self.auth_manager.users.pop(self.current_user)
                self.current_user = username
                message.append("Nombre de usuario actualizado")

        if password:
            if len(password) < 4:
                success = False
                message.append("La contraseña debe tener al menos 4 caracteres")
            else:
                self.auth_manager.users[self.current_user]["password"] = password
                message.append("Contraseña actualizada")

        if not message:
            message.append("No se realizaron cambios")

        self.page.snack_bar = ft.SnackBar(content=ft.Text(" ".join(message)))
        self.page.snack_bar.open = True
        self.page.snack_bar.bgcolor = ft.colors.GREEN_600 if success else ft.colors.RED_600
        self.page.update()

    def change_language(self, e):
        language = self.language_dropdown.value
        self.auth_manager.users[self.current_user]["language"] = language
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Idioma cambiado a {self.language_dropdown.options_dict[language].text}"))
        self.page.snack_bar.open = True
        self.page.snack_bar.bgcolor = ft.colors.GREEN_600
        self.page.update()

    def change_theme(self, e):
        theme = self.theme_dropdown.value
        self.page.theme_mode = ft.ThemeMode.LIGHT if theme == "light" else ft.ThemeMode.DARK
        self.auth_manager.users[self.current_user]["theme"] = theme
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Tema cambiado a {self.theme_dropdown.options_dict[theme].text}"))
        self.page.snack_bar.open = True
        self.page.snack_bar.bgcolor = ft.colors.GREEN_600
        self.page.update()

    def update_notifications(self, e):
        notifications = self.notifications_dropdown.value
        self.auth_manager.users[self.current_user]["notifications"] = notifications
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Notificaciones ajustadas a {self.notifications_dropdown.options_dict[notifications].text}"))
        self.page.snack_bar.open = True
        self.page.snack_bar.bgcolor = ft.colors.GREEN_600
        self.page.update()

    def update_map_prefs(self, e):
        units = self.units_dropdown.value
        location = self.location_field.value
        map_type = self.map_type_dropdown.value
        search_radius = int(self.search_radius_dropdown.value)
        visible_residues = [cb.data for cb in self.visible_residues_checklist.controls if cb.value]
        if not visible_residues:
            visible_residues = ["all"]

        self.auth_manager.users[self.current_user].update({
            "units": units,
            "location": location,
            "map_prefs": {
                "map_type": map_type,
                "search_radius": search_radius,
                "visible_residues": visible_residues
            }
        })

        self.page.snack_bar = ft.SnackBar(content=ft.Text("Preferencias del mapa guardadas"))
        self.page.snack_bar.open = True
        self.page.snack_bar.bgcolor = ft.colors.GREEN_600
        self.page.update()