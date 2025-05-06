#utils.py
import cv2
import tempfile
import os
import requests

API_URL = "http://localhost:8000/clasificador/predecir"  # Ajusta a tu endpoint real

def capture_image():
    # Abre la cámara por defecto (0)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("No se pudo capturar imagen de la cámara")
    # Guarda en un archivo temporal
    fd, path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    cv2.imwrite(path, frame)
    return path

def classify_image(image_path):
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
        resp = requests.post(API_URL, files=files)
    resp.raise_for_status()
    return resp.json()
