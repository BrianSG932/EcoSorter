#main.py
import flet as ft
from login import LoginScreen, AuthManager
from classify import ClassifyScreen
from settings import SettingsScreen
from map import MapScreen
from stats import StatsScreen
from camara import camara_component

import camarav2 as camara

class AppNavigator:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth_manager = AuthManager()
        self.screens = {
            "login": lambda: LoginScreen(self.page, self),
            "home": self.show_home,
            "classify": lambda: ClassifyScreen(self.page, self, self.auth_manager),
            "settings": lambda: SettingsScreen(self.page, self, self.auth_manager),
            "map": lambda: MapScreen(self.page, self, self.auth_manager),
            "stats": lambda: StatsScreen(self.page, self, self.auth_manager),
            "camara": lambda: camara_component(self, self.auth_manager)(self.page)
        }
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.current_screen = "home"
        self.navigate("login")



    def capturar_y_mostrar(self, e):
        try:
            base64img = camara.capturar_frame_base64()  # función que debes definir fuera de la clase
            self.camera_display.src_base64 = base64img
            self.page.update()
        except Exception as ex:
            print("Error capturando imagen:", ex)


    def navigate(self, screen_name):
        if screen_name in self.screens:
            self.current_screen = screen_name
            self.screens[screen_name]()
        else:
            self.page.clean()
            self.page.add(ft.Text("Pantalla no encontrada"))
        self.page.update()

    def toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.page.update()

    def show_home(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Inicio"

        welcome_text = ft.Text(
            "Bienvenido al Clasificador de Basura",
            size=34,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            font_family="Roboto",
            text_align=ft.TextAlign.CENTER
        )

        # Camera placeholder rectangle
        self.camera_display = ft.Image(
            width=300,
            height=200,
            fit=ft.ImageFit.COVER,
            #bgcolor=ft.Colors.GREY_300,
            #border_radius=10,
            #content=ft.Text("Cámara Habilitada", text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK54),
            #alignment=ft.alignment.center
        )

        # Camera icon button at top center
        camera_button = ft.IconButton(
            icon=ft.icons.CAMERA_ALT,
            bgcolor=ft.Colors.GREEN,
            on_click=self.capturar_y_mostrar
        )


        # Bottom navigation bar
        def create_nav_button(icon, label, screen, is_active):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.IconButton(
                            icon=icon,
                            icon_color=ft.Colors.WHITE if is_active else ft.Colors.GREY_400,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_600 if is_active else ft.Colors.GREY_800,
                                shape=ft.CircleBorder(),
                                padding=ft.padding.all(8)
                            ),
                            on_click=lambda e, s=screen: self.navigate(s),
                            width=50,
                            height=50,
                            animate_scale=True,
                            scale=1.0
                        ),
                        ft.Text(label, size=12, color=ft.Colors.WHITE if is_active else ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                ),
                alignment=ft.alignment.center
            )

        nav_bar = ft.Container(
            content=ft.Row(
                [
                    create_nav_button(ft.Icons.HOME, "Inicio", "home", self.current_screen == "home"),
                    create_nav_button(ft.Icons.MAP, "Mapa", "map", self.current_screen == "map"),
                    create_nav_button(ft.Icons.BAR_CHART, "Estadísticas", "stats", self.current_screen == "stats"),
                    create_nav_button(ft.Icons.SETTINGS, "Configuraciones", "settings", self.current_screen == "settings"),
                    create_nav_button(ft.Icons.LOGOUT, "Cerrar", "login", self.current_screen == "login")
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=0,
                width=self.page.width
            ),
            height=70
        )

        # Theme switcher
        theme_switcher = ft.IconButton(
            icon=ft.Icons.BRIGHTNESS_4,
            icon_color=ft.Colors.BLACK,
            style=ft.ButtonStyle(bgcolor=None),
            on_click=self.toggle_theme,
            tooltip="Cambiar Tema",
            icon_size=24,
            width=40,
            height=40
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([welcome_text, theme_switcher], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=20),
                        self.camera_display,
                        ft.Container(height=20),
                        ft.Row([camera_button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=30),
                        ft.Container(height=10),
                        nav_bar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=20,
                bgcolor=ft.Colors.GREY_100,
                expand=True
            )
        )
        self.page.update()

    def start_classification(self, e):
        dialog = ft.AlertDialog(
            title=ft.Text("Clasificar Residuos"),
            content=ft.Column([
                ft.Camera(
                    quality=80,
                    on_change=lambda e: self.handle_photo(e),
                    width=300,
                    height=200
                ),
                ft.ElevatedButton(
                    "Subir Foto",
                    on_click=lambda e: self.pick_file(),
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                )
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog()),
                ft.TextButton("Enviar", on_click=lambda e: self.navigate("classify"))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def handle_photo(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Foto capturada: {e.control.value}"))
        self.page.snack_bar.open = True
        self.page.update()

    def pick_file(self, e):
        file_picker = ft.FilePicker(on_result=lambda e: self.handle_file_picker_result(e))
        self.page.overlay.append(file_picker)
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])

    def handle_file_picker_result(self, e):
        if e.files:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Foto subida: {e.files[0].name}"))
            self.page.snack_bar.open = True
            self.page.update()
            self.navigate("classify")

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    AppNavigator(page)

if __name__ == "__main__":
    ft.app(target=main)