import flet as ft

class StatsScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.setup_ui()

    def setup_ui(self):
        # Fetch recycling stats for the logged-in user (default: "admin")
        username = "admin"  # Replace with actual user if auth is implemented
        stats = self.auth_manager.users.get(username, {}).get("recycling_stats", {
            "Plástico": 0, "Papel": 0, "Vidrio": 0, "Orgánico": 0,
            "Metal": 0, "Pilas": 0, "Electrónicos": 0
        })

        # Prepare bar chart data
        waste_types = list(stats.keys())
        values = list(stats.values())
        colors = [
            ft.Colors.BLUE_400, ft.Colors.GREEN_400, ft.Colors.RED_400,
            ft.Colors.BROWN_400, ft.Colors.GREY_400, ft.Colors.PURPLE_400,
            ft.Colors.ORANGE_400
        ]

        # Create bar chart groups (one group per waste type)
        bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=values[i],
                        width=30,
                        color=colors[i % len(colors)],
                        tooltip=f"{waste_types[i]}: {values[i]}",
                        border_radius=4
                    )
                ]
            )
            for i in range(len(waste_types))
        ]

        # Create bar chart
        chart = ft.BarChart(
            bar_groups=bar_groups,
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(waste_types[i], size=12, rotation=45))
                    for i in range(len(waste_types))
                ],
                labels_size=40
            ),
            left_axis=ft.ChartAxis(labels_size=40),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            max_y=max(values, default=1) + 1 if max(values) > 0 else 10,
            width=600,
            height=400
        )

        # Build UI
        self.container = ft.Column(
            [
                ft.Text("Estadísticas de Reciclaje", size=30, weight=ft.FontWeight.BOLD),
                chart,
                ft.ElevatedButton(
                    text="Volver",
                    on_click=lambda e: self.navigator.navigate("home"),
                    width=300,
                    bgcolor=ft.Colors.GREY_600,
                    color=ft.Colors.WHITE
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        self.page.clean()
        self.page.add(self.container)