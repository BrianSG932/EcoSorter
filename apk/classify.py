#classify.py
import flet as ft
import random
import requests
import base64
import io
from PIL import Image
from camara import camara_component
from utils import classify_image


class ClassifyScreen:
    def __init__(self, page: ft.Page, navigator, auth_manager):
        self.page = page
        self.navigator = navigator
        self.auth_manager = auth_manager
        self.image_path = None
        self.classification_result = None
        self.confidence = None
        self.setup_ui()

    def setup_ui(self):
        self.image_display = ft.Image(
            src="https://via.placeholder.com/300",
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        self.result_text = ft.Text(
            value="Selecciona una imagen para clasificar",
            size=20,
            color=ft.Colors.BLACK
        )
        self.recommendation_text = ft.Text(
            value="",
            size=16,
            color=ft.Colors.BLACK87,
            visible=False
        )
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)

        self.take_photo_button = ft.ElevatedButton(
            text="Tomar Foto",
            on_click=lambda e: self.navigator.navigate("camara"),
            width=145,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )
        self.upload_photo_button = ft.ElevatedButton(
            text="Subir Fotografía",
            on_click=self.upload_photo,
            width=145,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )
        self.analyze_button = ft.ElevatedButton(
            text="Analizar Imagen",
            on_click=self.classify_image,
            width=300,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            disabled=True
        )

        # Main content column
        main_content = ft.Column(
            [
                ft.Text("Clasificador de Residuos", size=30, weight=ft.FontWeight.BOLD),
                self.image_display,
                self.result_text,
                self.recommendation_text,
                ft.Row(
                    [self.take_photo_button, self.upload_photo_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                self.analyze_button,
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
        self.container = ft.Stack(
            [
                main_content,
                ft.Container(
                    content=back_arrow,
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(left=10, top=10)
                )
            ],
            expand=True
        )

        self.page.clean()
        self.page.add(self.container)

    def take_photo(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def upload_photo(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.image_path = e.files[0].path
            try:
                # Mostrar vista previa de imagen
                with open(self.image_path, "rb") as f:
                    img = Image.open(f)
                    img = img.resize((300, 300))
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    self.image_display.src_base64 = img_base64
                    self.result_text.value = "Clasificando..."
                    self.result_text.color = ft.Colors.BLACK
                    self.page.update()

                # Clasificación real vía API
                resultado = classify_image(self.image_path)
                material = resultado["clase_predicha"]["material"]
                confianza = resultado["clase_predicha"]["confianza"]

                self.result_text.value = f"Clasificado: {material} ({confianza}%)"
                self.result_text.color = ft.Colors.GREEN

                # Mostrar recomendación si aplica
                recomendaciones = {
                    "Plástico": "Lava los envases plásticos...",
                    "Papel": "Asegúrate de que el papel esté limpio...",
                    "Vidrio": "Deposita botellas y frascos...",
                    "Orgánico": "Coloca los residuos orgánicos...",
                    "Metal": "Limpia latas y envases metálicos...",
                    "Pilas": "Lleva las pilas a un punto de recolección...",
                    "Electrónicos": "Entrega dispositivos electrónicos..."
                }

                self.recommendation_text.value = f"Recomendación: {recomendaciones.get(material, 'No hay recomendación disponible.')}"
                self.recommendation_text.visible = True

            except Exception as ex:
                self.result_text.value = f"Error: {str(ex)}"
                self.result_text.color = ft.Colors.RED
                self.recommendation_text.visible = False

            self.page.update()

    def classify_image(self, e):
        if not self.image_path:
            self.result_text.value = "Por favor, selecciona una imagen primero."
            self.result_text.color = ft.Colors.RED
            self.recommendation_text.visible = False
            self.page.update()
            return

        waste_types = ["Plástico", "Papel", "Vidrio", "Orgánico", "Metal", "Pilas", "Electrónicos"]
        self.classification_result = random.choice(waste_types)
        self.confidence = random.uniform(0.7, 0.95)

        username = "admin"
        if username in self.auth_manager.users:
            self.auth_manager.users[username]["recycling_stats"][self.classification_result] += 1

        self.result_text.value = f"Clasificado: {self.classification_result} ({self.confidence:.0%})"
        self.result_text.color = ft.Colors.GREEN

        recommendations = {
            "Plástico": "Lava los envases plásticos y deposítalos en el contenedor azul. Evita mezclar plásticos no reciclables.",
            "Papel": "Asegúrate de que el papel esté limpio y seco, y colócalo en el contenedor de papel/cartón.",
            "Vidrio": "Deposita botellas y frascos de vidrio en el contenedor verde. No incluyas cristales o espejos.",
            "Orgánico": "Coloca los residuos orgánicos en el contenedor marrón o en un compostador doméstico.",
            "Metal": "Limpia latas y envases metálicos y deposítalos en el contenedor amarillo.",
            "Pilas": "Lleva las pilas a un punto de recolección especializado, como en supermercados o centros de reciclaje.",
            "Electrónicos": "Entrega dispositivos electrónicos en puntos de recolección específicos o programas de reciclaje."
        }
        self.recommendation_text.value = f"Recomendación: {recommendations.get(self.classification_result, 'No hay recomendaciones disponibles.')}"
        self.recommendation_text.visible = True

        try:
            server_key = "YOUR_FCM_SERVER_KEY"
            fcm_token = "YOUR_FCM_TOKEN"
            if server_key != "YOUR_FCM_SERVER_KEY" and fcm_token != "YOUR_FCM_TOKEN":
                headers = {"Authorization": f"key={server_key}", "Content-Type": "application/json"}
                payload = {
                    "to": fcm_token,
                    "notification": {
                        "title": "Clasificación Completada",
                        "body": f"Residuo clasificado como {self.classification_result} ({self.confidence:.0%})."
                    }
                }
                response = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)
                response.raise_for_status()
            else:
                self.result_text.value += " (Notificación simulada)"
        except Exception as ex:
            self.result_text.value += f" (Error en notificación: {str(ex)})"

        self.page.update()