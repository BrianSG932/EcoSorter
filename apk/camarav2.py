#camara.py
import cv2
import base64
from PIL import Image
import io
import numpy as np

def capturar_frame_base64():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("No se pudo capturar imagen de la cámara.")

    # Convertir BGR → RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imagen = Image.fromarray(frame)
    imagen = imagen.resize((300, 200))

    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return imagen_base64
