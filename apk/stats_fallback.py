import flet as ft
from login import AuthManager

class StatsScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.current_user = "admin"  # Simulación del usuario actual
        self.setup_ui()

    def setup_ui(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Estadísticas"

        # Obtener estadísticas del usuario
        stats = self.auth_manager.users.get(self.current_user, {}).get("recycling_stats", {
            "Plástico": 0, "Papel": 0, "Vidrio": 0, "Orgánico": 0, "Metal": 0, "Pilas": 0, "Electrónicos": 0
        })

        # Calcular impacto ambiental (CO2 ahorrado en kg)
        co2_factors = {
            "Plástico": 2.0,  # kg de CO2 ahorrado por kg reciclado
            "Papel": 1.0,
            "Vidrio": 0.3,
            "Orgánico": 0.5,
            "Metal": 4.0,
            "Pilas": 10.0,
            "Electrónicos": 5.0
        }
        total_co2 = sum(stats[residue] * co2_factors[residue] for residue in stats)
        total_weight = sum(stats[residue] for residue in stats)

        # Lista de estadísticas
        stats_list = ft.ListView(
            controls=[
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{residue}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Peso reciclado: {stats[residue]:.2f} kg"),
                                ft.Text(f"CO2 ahorrado: {stats[residue] * co2_factors[residue]:.2f} kg")
                            ],
                            spacing=5
                        ),
                        padding=10
                    )
                ) for residue in stats
            ],
            spacing=10,
            padding=10,
            expand=True
        )

        # Botón de volver
        back_button = ft.ElevatedButton(
            text="Volver al Inicio",
            icon=ft.Icons.HOME,
            on_click=lambda e: self.navigator.navigate("home"),
            width=300,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE
        )

        # Contenedor principal
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Estadísticas de Reciclaje", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ft.Text("Resumen de tus esfuerzos de reciclaje.", size=16, color=ft.Colors.BLACK54),
                        ft.Text(f"Total reciclado: {total_weight:.2f} kg", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"CO2 ahorrado: {total_co2:.2f} kg", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Detalles por tipo de residuo:", size=16, weight=ft.FontWeight.BOLD),
                        stats_list,
                        back_button
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