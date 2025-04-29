import flet as ft
import base64

def main(page: ft.Page):
    # Abrir desde subcarpeta "assets"
    with open("assets/ejemplo.jpg", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Mostrar imagen en pantalla
    page.add(ft.Image(src_base64=f"data:image/jpeg;base64,{img_base64}"))

# Ejecutar en navegador y servir la carpeta "assets"
ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")