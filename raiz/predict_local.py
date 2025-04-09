
#predict_local.py
import numpy as np
import cv2
#import tensorflow as tf
import keras
from keras.models import load_model


# === CONFIGURACIÓN ===
MODEL_PATH = "app/models/modelo_clasificador_materiales.h5"
IMG_PATH = "imagen_prueba.jpg"  # ⚠️ CAMBIA este nombre por el de tu imagen
IMG_SIZE = (64, 64)
CLASES = ['papel', 'plastico', 'vidrio', 'metal']  # Ajusta según tu dataset

# === CARGAR MODELO ===
print("Cargando modelo...")
modelo = load_model(MODEL_PATH)

# === CARGAR Y PROCESAR IMAGEN ===
print("Procesando imagen...")
imagen = cv2.imread(IMG_PATH)
imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen = cv2.resize(imagen, IMG_SIZE)
imagen = imagen / 255.0
imagen = np.expand_dims(imagen, axis=0)

# === PREDICCIÓN ===
print("Haciendo predicción...")
prediccion = modelo.predict(imagen)[0]
indice_pred = np.argmax(prediccion)
confianza = float(prediccion[indice_pred])
material = CLASES[indice_pred]

print(f"✅ Material detectado: {material}")
print(f"🔎 Precisión del modelo: {confianza:.2f}")
