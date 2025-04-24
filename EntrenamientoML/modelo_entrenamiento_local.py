# modelo_entrenamiento_local.py
import os
import numpy as np
import tensorflow as tf
from keras import layers, models
from sklearn.model_selection import train_test_split
import cv2
import datetime
import json

# Ruta local al dataset
DATASET_PATH = "G:\Mi unidad\EcoSorter\archive\realwaste-main\RealWaste"
IMG_SIZE = (64, 64)

# Verificar que la ruta existe
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"No se encontró el dataset en: {DATASET_PATH}")

# Detectar clases
clases = sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))])
num_clases = len(clases)

# Preprocesamiento
images = []
labels = []

print(" Cargando imágenes...")
for clase_idx, clase in enumerate(clases):
    clase_path = os.path.join(DATASET_PATH, clase)
    print(f"🔍 Procesando clase '{clase}' con {len(os.listdir(clase_path))} imágenes...")
    for img_file in os.listdir(clase_path):
        img_path = os.path.join(clase_path, img_file)
        try:
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            img = img / 255.0
            images.append(img)
            labels.append(clase_idx)
        except Exception as e:
            print(f"Error al procesar {img_path}: {e}")

X = np.array(images)
y = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Modelo CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.Dense(num_clases, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

print(" Entrenando el modelo...")
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Crear carpeta si no existe
os.makedirs("app/models", exist_ok=True)

# Guardar modelo
output_path = "app/models/modelo_clasificador_materiales.h5"
model.save(output_path)
print(f"Modelo guardado en {output_path}")

# Guardar las clases en JSON
clases_path = "app/models/clases.json"
with open(clases_path, "w") as f:
    json.dump(clases, f)
print(f"Clases guardadas en {clases_path}: {clases}")