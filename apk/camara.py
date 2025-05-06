#camara.py
import flet as ft
from utils import capture_image, classify_image
import os
import base64
import shutil 

def camara_component(navigator, auth_manager):
    def camara(page: ft.Page):
        page.title = "EcoSorter Mobile"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.padding = 20

        image_view = ft.Image(width=300, height=300)
        result_text = ft.Text("", size=18)

        def on_capture_click(e):
            try:
                path = capture_image()

                # Crea carpeta temp si no existe
                if not os.path.exists("temp"):
                    os.makedirs("temp")

                # Copia la imagen a ./temp/ con nombre unico
                final_path = os.path.join("temp", os.path.basename(path))
                shutil.copy(path, final_path)

                # Mostrar imagen
                image_view.src = f"/temp/{os.path.basename(path)}"
                page.update()
                result_text.value = "Clasificando..."
                page.update()

                result = classify_image(path)

                mat = result["clase_predicha"]["material"]
                conf = result["clase_predicha"]["confianza"]
                result_text.value = f"Material: {mat}\nConfianza: {conf}%"

            except Exception as err:
                result_text.value = f"Error: {err}"

            page.update()

        capture_btn = ft.ElevatedButton("Tomar foto y clasificar", on_click=on_capture_click)

        page.clean()
        page.add(
            ft.Column([
                ft.Text("Clasificador en vivo", size=30, weight=ft.FontWeight.BOLD),
                capture_btn,
                ft.Container(image_view, margin=(20, 0, 0, 0)),
                result_text,
                ft.ElevatedButton(
                    text="Volver",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: navigator.navigate("home"),
                    width=300,
                    bgcolor=ft.Colors.GREY_600,
                    color=ft.Colors.WHITE
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return camara
