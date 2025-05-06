import flet as ft
import os
import requests
from login import AuthManager
from pyfcm import FCMNotification

class MapScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.current_user = "admin"
        self.setup_ui()

    def setup_ui(self):
        self.page.clean()
        self.page.title = "Clasificador de Basura - Mapa"

        default_location = self.auth_manager.users.get(self.current_user, {}).get("location", "Ciudad de México")
        self.location_field = ft.TextField(
            label="Ubicación",
            value=default_location,
            width=300,
            on_change=self.update_map
        )

        self.residue_filter = ft.Dropdown(
            label="Filtrar por Residuo",
            options=[
                ft.dropdown.Option("all", "Todos"),
                ft.dropdown.Option("Plástico", "Plástico"),
                ft.dropdown.Option("Papel", "Papel"),
                ft.dropdown.Option("Vidrio", "Vidrio"),
                ft.dropdown.Option("Orgánico", "Orgánico"),
                ft.dropdown.Option("Metal", "Metal"),
                ft.dropdown.Option("Pilas", "Pilas"),
                ft.dropdown.Option("Electrónicos", "Electrónicos")
            ],
            value="all",
            width=300,
            on_change=self.update_map
        )

        self.locations_list = ft.ListView(expand=True, spacing=10, padding=10)

        self.map_container = ft.Container(
            content=ft.WebView(
                url="",
                expand=True,
                on_page_started=lambda e: self.page.show_snack_bar(ft.SnackBar(ft.Text("Cargando mapa...")))
            ),
            width=600,
            height=400,
            border=ft.border.all(2, ft.colors.BLUE_600),
            border_radius=10
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
                ft.Text("Mapa de Centros de Reciclaje", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.Text("Encuentra centros de reciclaje y contenedores cercanos.", size=16, color=ft.colors.BLACK54),
                ft.Row(
                    [self.location_field, self.residue_filter],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.Row(
                    [
                        self.map_container,
                        ft.Container(
                            content=self.locations_list,
                            width=300,
                            height=400,
                            border=ft.border.all(2, ft.colors.GREY_400),
                            border_radius=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
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

        self.update_map(None)
        self.page.update()

    def get_recycling_centers(self, location, radius):
        api_key = "YOUR_GOOGLE_MAPS_API_KEY"
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        geocode_response = requests.get(geocode_url).json()
        if geocode_response["status"] != "OK":
            return []

        coords = geocode_response["results"][0]["geometry"]["location"]
        lat, lng = coords["lat"], coords["lng"]

        places_url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lng}&radius={radius}&keyword=recycling+center&key={api_key}"
        )
        places_response = requests.get(places_url).json()
        if places_response["status"] != "OK":
            return []

        locations = []
        for place in places_response.get("results", [])[:5]:
            locations.append({
                "name": place["name"],
                "coords": [place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]],
                "address": place.get("vicinity", "Sin dirección"),
                "hours": "No disponible" if not place.get("opening_hours") else "Consultar horarios",
                "residues": ["Plástico", "Papel", "Vidrio", "Metal"]
            })
        return locations

    def update_map(self, e):
        map_prefs = self.auth_manager.users.get(self.current_user, {}).get("map_prefs", {})
        map_type = map_prefs.get("map_type", "roadmap")
        radius = map_prefs.get("search_radius", 5000)
        visible_residues = map_prefs.get("visible_residues", ["all"])

        location = self.location_field.value
        locations = self.get_recycling_centers(location, radius)

        residue_type = self.residue_filter.value
        if residue_type != "all" and residue_type not in visible_residues:
            locations = [loc for loc in locations if residue_type in loc["residues"]]

        center_coords = [19.432, -99.135]
        if "nueva york" in location.lower():
            center_coords = [40.7128, -74.0060]
        elif "londres" in location.lower():
            center_coords = [51.5074, -0.1278]

        api_key = "YOUR_GOOGLE_MAPS_API_KEY"
        map_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mapa de Reciclaje</title>
            <style>
                #map {{ height: 100%; width: 100%; }}
                html, body {{ height: 100%; margin: 0; padding: 0; }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                function initMap() {{
                    const map = new google.maps.Map(document.getElementById("map"), {{
                        center: {{ lat: {center_coords[0]}, lng: {center_coords[1]} }},
                        zoom: 13,
                        mapTypeId: "{map_type}",
                    }});
                    const directionsService = new google.maps.DirectionsService();
                    const directionsRenderer = new google.maps.DirectionsRenderer();
                    directionsRenderer.setMap(map);
                    const locations = {str(locations).replace("'", '"')};
                    locations.forEach((loc, index) => {{
                        const marker = new google.maps.Marker({{
                            position: {{ lat: loc.coords[0], lng: loc.coords[1] }},
                            map: map,
                            title: loc.name,
                        }});
                        const infowindow = new google.maps.InfoWindow({{
                            content: `
                                <b>${{loc.name}}</b><br>
                                Dirección: ${{loc.address}}<br>
                                Horarios: ${{loc.hours}}<br>
                                Residuos: ${{loc.residues.join(", ")}}<br>
                                <button onclick="showDirections({center_coords[0]}, {center_coords[1]}, ${{loc.coords[0]}}, ${{loc.coords[1]}})">Mostrar Ruta</button>
                            `,
                        }});
                        marker.addListener("click", () => {{
                            infowindow.open(map, marker);
                        }});
                    }});
                    window.showDirections = function(startLat, startLng, endLat, endLng) {{
                        directionsService.route({{
                            origin: {{ lat: startLat, lng: startLng }},
                            destination: {{ lat: endLat, lng: endLng }},
                            travelMode: google.maps.TravelMode.DRIVING,
                        }}, (response, status) => {{
                            if (status === "OK") {{
                                directionsRenderer.setDirections(response);
                            }} else {{
                                alert("Error al calcular la ruta: " + status);
                            }}
                        }});
                    }};
                }}
            </script>
            <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places&callback=initMap" async defer></script>
        </body>
        </html>
        """

        map_file = os.path.abspath("map.html")
        with open(map_file, "w", encoding="utf-8") as f:
            f.write(map_html)

        self.map_container.content.url = f"file://{map_file}"

        self.locations_list.controls.clear()
        for loc in locations:
            self.locations_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(loc["name"], weight=ft.FontWeight.BOLD),
                                ft.Text(f"Dirección: {loc['address']}"),
                                ft.Text(f"Horarios: {loc['hours']}"),
                                ft.Text(f"Residuos: {', '.join(loc['residues'])}")
                            ],
                            spacing=5
                        ),
                        padding=10
                    )
                )
            )

        self.auth_manager.users[self.current_user]["location"] = self.location_field.value

        notification_freq = self.auth_manager.users.get(self.current_user, {}).get("notifications", "daily")
        if notification_freq != "off" and locations:
            nearest_center = locations[0]["name"]
            self.send_push_notification(
                title="Centro de Reciclaje Cercano",
                body=f"Visita {nearest_center} para reciclar tus residuos en {location}."
            )

        self.page.update()

    def send_push_notification(self, title, body):
        api_key = "YOUR_FCM_SERVER_KEY"
        push_service = FCMNotification(api_key=api_key)
        registration_id = "YOUR_FCM_TOKEN"

        try:
            result = push_service.notify_single_device(
                registration_id=registration_id,
                message_title=title,
                message_body=body
            )
            print(f"Notificación enviada: {result}")
        except Exception as e:
            print(f"Error al enviar notificación: {e}")
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Notificación: {title} - {body}")))