import numpy as np
import cv2
from fastapi import UploadFile
from io import BytesIO

# Simulación de modelo (sustituir luego por el real)
async def predecir_residuo(imagen: UploadFile):
    contenido = await imagen.read()
    img_np = np.frombuffer(contenido, np.uint8)
    imagen_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Aquí va la lógica real del modelo
    resultado = "plástico PET"
    confianza = 0.93

    return {
        "material": resultado,
        "confianza": confianza
    }
