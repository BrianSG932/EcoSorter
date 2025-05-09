#mapa.py
import flet as ft
import os
from flet_webview import WebView  # nuevo import

def main(page: ft.Page):
    page.title = "Mapa con OpenStreetMap"
    page.window_width = 800
    page.window_height = 600

    html_file_path = os.path.abspath("F:/respaldopc/EcoSorter/apk/mapa/mapa.html")

    # Ahora usamos WebView del nuevo paquete
    mapa = WebView(url=f"file://{html_file_path}", expand=True)

    page.add(mapa)

ft.app(target=main)