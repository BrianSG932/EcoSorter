import flet as ft
from login import AuthManager

class StatsScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.current_user = "admin"
        self.setup_ui()

    def setup_ui(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Estadísticas"

        stats = self.auth_manager.users.get(self.current_user, {}).get("recycling_stats", {
            "Plástico": 0, "Papel": 0, "Vidrio": 0, "Orgánico": 0, "Metal": 0, "Pilas": 0, "Electrónicos": 0
        })

        co2_factors = {
            "Plástico": 2.0,
            "Papel": 1.0,
            "Vidrio": 0.3,
            "Orgánico": 0.5,
            "Metal": 4.0,
            "Pilas": 10.0,
            "Electrónicos": 5.0
        }
        total_co2 = sum(stats[residue] * co2_factors[residue] for residue in stats)
        total_weight = sum(stats[residue] for residue in stats)

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

        # Main content column
        main_content = ft.Column(
            [
                ft.Text("Estadísticas de Reciclaje", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Text("Resumen de tus esfuerzos de reciclaje.", size=16, color=ft.Colors.BLACK54),
                ft.Text(f"Total reciclado: {total_weight:.2f} kg", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"CO2 ahorrado: {total_co2:.2f} kg", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Detalles por tipo de residuo:", size=16, weight=ft.FontWeight.BOLD),
                stats_list,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
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
                bgcolor=ft.Colors.GREY_100,
                border_radius=10
            )
        )
        self.page.update()