#modeloml.py api
import tensorflow as tf
import numpy as np
import cv2
import json
from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import os

# Cargar el modelo entrenado
def cargar_modelo_y_clases():
    modelo_path = "app/models/modelo_clasificador_materiales.h5"
    modelo = tf.keras.models.load_model(modelo_path)
    with open("app/models/clases.json", "r") as f:
        clases = json.load(f)
    return modelo, clases

IMG_SIZE = (64, 64)

def predecir_imagen(ruta_imagen, modelo, clases):
    IMG_SIZE = (64, 64)
    img = Image.open(ruta_imagen).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediccion = modelo.predict(img_array)[0]
    idx = int(np.argmax(prediccion))
    clase = clases[idx]
    confianza = float(prediccion[idx])
    return {"material": clase, "confianza": round(confianza * 100, 2)}