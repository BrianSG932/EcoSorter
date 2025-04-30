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
        self.navigate("login")

    def navigate(self, screen_name):
        if screen_name in self.screens:
            self.screens[screen_name]()
        else:
            self.page.clean()
            self.page.add(ft.Text("Pantalla no encontrada"))
        self.page.update()

    def show_home(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Inicio"

        welcome_text = ft.Text(
            "Bienvenido al Clasificador de Basura",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        classify_button = ft.ElevatedButton(
            text="Clasificar Residuos",
            icon=ft.Icons.RECYCLING,
            on_click=lambda e: self.navigate("classify"),
            width=300,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )

        map_button = ft.ElevatedButton(
            text="Ver Mapa de Reciclaje",
            icon=ft.Icons.MAP,
            on_click=lambda e: self.navigate("map"),
            width=300,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE
        )

        stats_button = ft.ElevatedButton(
            text="Ver Estadísticas",
            icon=ft.Icons.BAR_CHART,
            on_click=lambda e: self.navigate("stats"),
            width=300,
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE
        )

        settings_button = ft.ElevatedButton(
            text="Configuraciones",
            icon=ft.Icons.SETTINGS,
            on_click=lambda e: self.navigate("settings"),
            width=300,
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE
        )

        logout_button = ft.ElevatedButton(
            text="Cerrar Sesión",
            icon=ft.Icons.LOGOUT,
            on_click=lambda e: self.navigate("login"),
            width=300,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        welcome_text,
                        ft.Text("Elige una opción:", size=20, color=ft.Colors.BLACK54),
                        classify_button,
                        map_button,
                        stats_button,
                        settings_button,
                        logout_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=20,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10
            )
        )
        self.page.update()

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    AppNavigator(page)

if __name__ == "__main__":
    ft.app(target=main)