import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
import datetime
import cv2
from google.colab import files
import zipfile

# 1. Configuración de MongoDB (usar Atlas para Colab)
MONGO_URI = "mongodb+srv://<usuario>:<contraseña>@cluster0.mongodb.net/EcoSorter?retryWrites=true&w=majority"  # Cambia por tu URI de MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['EcoSorter']
modelo_ml_collection = db['Modelo_ML']
predicciones_collection = db['Predicciones']

# 2. Subir el dataset comprimido desde tu máquina
print("Sube un archivo .zip con las imágenes organizadas en subcarpetas (ej. plastico/, vidrio/, tela/)")
uploaded = files.upload()

# Descomprimir el archivo
zip_file = list(uploaded.keys())[0]
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall('/content/dataset')
os.remove(zip_file)  # Eliminar el .zip después de extraer

DATASET_PATH = "/content/dataset/"
IMG_SIZE = (64, 64)
clases = sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))])
num_clases = len(clases)

# 3. Cargar y preprocesar las imágenes
images = []
labels = []

print("Cargando imágenes...")
for clase_idx, clase in enumerate(clases):
    clase_path = os.path.join(DATASET_PATH, clase)
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

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Total de imágenes cargadas: {len(X)}")
print(f"Entrenamiento: {len(X_train)}, Prueba: {len(X_test)}")
print(f"Clases detectadas: {clases}")

# 4. Configurar GPU en Colab
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("GPU configurada para el entrenamiento.")
else:
    print("No se detectó GPU, usando CPU.")

# 5. Definir un modelo CNN más robusto
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.Dense(num_clases, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# 6. Entrenar el modelo
print("Entrenando el modelo...")
history = model.fit(X_train, y_train, 
                    epochs=20, 
                    batch_size=32, 
                    validation_data=(X_test, y_test))

# Evaluar el modelo
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Precisión en el conjunto de prueba: {test_accuracy:.4f}")

# 7. Guardar el modelo en Colab
model_path = "/content/modelo_clasificador_materiales.h5"
model.save(model_path)
print(f"Modelo guardado en: {model_path}")

# 8. Almacenar información del modelo en MongoDB
modelo_data = {
    "id_modelo": modelo_ml_collection.count_documents({}) + 1,
    "nombre": "Clasificador de Materiales Multi-Clase",
    "tipo": "clasificación",
    "fecha_entrenamiento": datetime.datetime.now(),
    "parametros": {
        "epochs": 20,
        "batch_size": 32,
        "optimizer": "adam",
        "loss": "sparse_categorical_crossentropy",
        "num_clases": num_clases
    },
    "ruta_archivo": model_path,
    "precision": float(test_accuracy)
}
modelo_ml_collection.insert_one(modelo_data)
print("Información del modelo almacenada en MongoDB.")

# 9. Hacer predicciones y guardarlas en MongoDB
predicciones = model.predict(X_test)
for i, pred in enumerate(predicciones):
    pred_class_idx = np.argmax(pred)
    confianza = float(pred[pred_class_idx])
    pred_class_name = clases[pred_class_idx]
    prediccion_data = {
        "id_prediccion": predicciones_collection.count_documents({}) + 1,
        "id_modelo": modelo_data["id_modelo"],
        "id_recoleccion": None,
        "fecha_prediccion": datetime.datetime.now(),
        "entrada": {"imagen": f"test_image_{i}"},
        "resultado": pred_class_name,
        "precision": confianza
    }
    predicciones_collection.insert_one(prediccion_data)

print(f"{len(predicciones)} predicciones almacenadas en MongoDB.")

# 10. Descargar el modelo desde Colab
files.download(model_path)

# Cerrar conexión a MongoDB
client.close()