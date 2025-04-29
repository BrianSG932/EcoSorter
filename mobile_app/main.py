#main.py
import flet as ft
from utils import capture_image, classify_image
import os
import base64
import shutil 

def main(page: ft.Page):
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

            # Copia la imagen a ./temp/ con nombre único
            final_path = os.path.join("temp", os.path.basename(path))
            shutil.copy(path, final_path)

            # Mostrar imagen con ruta accesible para Flet
            image_view.src = f"/temp/{os.path.basename(path)}"

            page.update()
            result_text.value = "Clasificando..."
            page.update()

            result = classify_image(path)

            mat = result["clase_predicha"]["material"]
            conf = result["clase_predicha"]["confianza"]
            result_text.value = f"Material: {mat}\nConfianza: {conf}%"

            # Puedes eliminar si ya no necesitas los archivos
            # os.remove(path)

        except Exception as err:
            result_text.value = f"Error: {err}"

        page.update()

        #os.remove(path)

    capture_btn = ft.ElevatedButton("Tomar foto y clasificar", on_click=on_capture_click)

    

    page.add(
        ft.Column([
            capture_btn,
            ft.Container(image_view, margin=(20, 0, 0, 0)),
            result_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
  # Puedes usar MOBILE_BROWSER o NATIVE si lo configuras
