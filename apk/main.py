import flet as ft
from login import LoginScreen, AuthManager
from classify import ClassifyScreen
from settings import SettingsScreen
from map import MapScreen
from stats import StatsScreen

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
            "stats": lambda: StatsScreen(self.page, self, self.auth_manager)
        }
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.navigate("login")

    def navigate(self, screen_name):
        if screen_name in self.screens:
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
            font_family="Roboto"
        )

        def create_icon_button(icon, color, on_click, tooltip, label):
            return ft.Card(
                content=ft.Column([
                    ft.IconButton(
                        icon=icon,
                        icon_color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            bgcolor=color,
                            shape=ft.CircleBorder(),
                            elevation=2
                        ),
                        on_click=on_click,
                        tooltip=tooltip,
                        width=60,
                        height=60,
                        animate_scale=True,
                        scale=1.0
                    ),
                    ft.Text(label, size=14, color=ft.Colors.BLACK54, text_align=ft.TextAlign.CENTER, max_lines=2)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                elevation=4
            )

        # Navigation icons in a responsive row
        icon_row = ft.ResponsiveRow([
            ft.Column(col={"sm": 12, "md": 2.4}, controls=[
                create_icon_button(
                    ft.Icons.RECYCLING, ft.Colors.GREEN_600, lambda e: self.navigate("classify"),
                    "Clasificar Residuos", "Clasificar"
                )
            ]),
            ft.Column(col={"sm": 12, "md": 2.4}, controls=[
                create_icon_button(
                    ft.Icons.MAP, ft.Colors.BLUE_600, lambda e: self.navigate("map"),
                    "Ver Mapa de Reciclaje", "Mapa"
                )
            ]),
            ft.Column(col={"sm": 12, "md": 2.4}, controls=[
                create_icon_button(
                    ft.Icons.BAR_CHART, ft.Colors.PURPLE_600, lambda e: self.navigate("stats"),
                    "Ver Estadísticas", "Estadísticas"
                )
            ]),
            ft.Column(col={"sm": 12, "md": 2.4}, controls=[
                create_icon_button(
                    ft.Icons.SETTINGS, ft.Colors.ORANGE_600, lambda e: self.navigate("settings"),
                    "Configuraciones", "Config."
                )
            ]),
            ft.Column(col={"sm": 12, "md": 2.4}, controls=[
                create_icon_button(
                    ft.Icons.LOGOUT, ft.Colors.RED_600, lambda e: self.navigate("login"),
                    "Cerrar Sesión", "Salir"
                )
            ])
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

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
                        ft.Row([ft.Container(expand=True), welcome_text, theme_switcher], alignment=ft.MainAxisAlignment.END),
                        ft.Text("Elige una opción:", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK54),
                        icon_row,
                        ft.Container(height=30)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30
                ),
                padding=30,
                bgcolor=ft.Colors.GREY_100,
                expand=True
            )
        )
        self.page.update()

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    AppNavigator(page)

if __name__ == "__main__":
    ft.app(target=main)