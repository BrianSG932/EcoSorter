#mongoDB(EcoSorter)/ConexionBD.py
from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB (local por defecto, puerto 27017)
client = MongoClient('mongodb+srv://BrianSG230:KmAq8alNdVqEbCJ9@ecosorter.cjb4gde.mongodb.net/')
db = client['EcoSorter']  # Crear o conectar a la base de datos EcoSorter

# Eliminar colecciones existentes para empezar desde cero (opcional)
db.drop_collection('Usuarios')
db.drop_collection('Materiales')
db.drop_collection('Recolecciones')
db.drop_collection('Detalle_Recoleccion')
db.drop_collection('Procesos_Reciclaje')
db.drop_collection('Reportes')
db.drop_collection('Modelo_ML')
db.drop_collection('Predicciones')
db.drop_collection('Inventario')  # Nueva colección

# Crear colecciones e insertar datos iniciales de ejemplo
# 1. Usuarios
usuarios = db['Usuarios']
usuarios.insert_many([
    {
        "id_usuario": 1,
        "nombre": "Juan Pérez",
        "tipo_usuario": "residente",
        "email": "juan.perez@example.com",
        "telefono": "123456789",
        "direccion": "Calle Falsa 123",
        "fecha_registro": datetime(2025, 3, 1)
    },
    {
        "id_usuario": 2,
        "nombre": "EcoEmpresa SA",
        "tipo_usuario": "empresa",
        "email": "contacto@ecoempresa.com",
        "telefono": "987654321",
        "direccion": "Av. Industrial 456",
        "fecha_registro": datetime(2025, 3, 2)
    }
])

# 2. Materiales
materiales = db['Materiales']
materiales.insert_many([
    {
        "id_material": 1,
        "nombre": "Plástico PET",
        "descripcion": "Plástico reciclable de botellas",
        "categoria": "Plástico",
        "valor_por_kg": 0.5
    },
    {
        "id_material": 2,
        "nombre": "Vidrio transparente",
        "descripcion": "Vidrio reciclable de envases",
        "categoria": "Vidrio",
        "valor_por_kg": 0.3
    }
])

# 3. Recolecciones
recolecciones = db['Recolecciones']
recolecciones.insert_many([
    {
        "id_recoleccion": 1,
        "id_usuario": 1,
        "fecha_recoleccion": datetime(2025, 3, 20, 10, 0),
        "ubicacion": "Calle Falsa 123",
        "estado": "completada",
        "peso_total": 10.0
    }
])

# 4. Detalle_Recoleccion
detalle_recoleccion = db['Detalle_Recoleccion']
detalle_recoleccion.insert_many([
    {
        "id_detalle": 1,
        "id_recoleccion": 1,
        "id_material": 1,
        "cantidad": 6.0,
        "observaciones": "Botellas limpias"
    },
    {
        "id_detalle": 2,
        "id_recoleccion": 1,
        "id_material": 2,
        "cantidad": 4.0,
        "observaciones": "Frascos intactos"
    }
])

# 5. Procesos_Reciclaje
procesos_reciclaje = db['Procesos_Reciclaje']
procesos_reciclaje.insert_many([
    {
        "id_proceso": 1,
        "id_recoleccion": 1,
        "id_material": 1,
        "tipo_proceso": "trituración",
        "fecha_inicio": datetime(2025, 3, 21, 9, 0),
        "fecha_fin": datetime(2025, 3, 21, 10, 0),
        "costo": 5.0,
        "resultado": "Material triturado"
    }
])

# 6. Reportes
reportes = db['Reportes']
reportes.insert_many([
    {
        "id_reporte": 1,
        "id_usuario": 2,
        "fecha_generacion": datetime(2025, 3, 25, 15, 0),
        "tipo_reporte": "mensual",
        "contenido": {"total_kg": 10.0, "categorias": {"Plástico": 6.0, "Vidrio": 4.0}}
    }
])

# 7. Modelo_ML
modelo_ml = db['Modelo_ML']
modelo_ml.insert_many([
    {
        "id_modelo": 1,
        "nombre": "Clasificador de Materiales",
        "tipo": "clasificación",
        "fecha_entrenamiento": datetime(2025, 3, 15),
        "parametros": {"learning_rate": 0.01, "epochs": 50},
        "ruta_archivo": "/models/clasificador_v1.pkl"
    }
])

# 8. Predicciones
predicciones = db['Predicciones']
predicciones.insert_many([
    {
        "id_prediccion": 1,
        "id_modelo": 1,
        "id_recoleccion": 1,
        "fecha_prediccion": datetime(2025, 3, 20, 12, 0),
        "entrada": {"imagen": "data/img1.jpg", "sensor_densidad": 1.2},
        "resultado": "Plástico PET",
        "precision": 0.95
    }
])

# 9. Inventario (Nueva colección como mejora)
inventario = db['Inventario']
inventario.insert_many([
    {
        "id_inventario": 1,
        "id_material": 1,
        "cantidad_disponible": 6.0,  # Cantidad procesada del proceso anterior
        "fecha_actualizacion": datetime(2025, 3, 21, 10, 0),
        "estado": "listo para venta",
        "ubicacion_almacen": "Almacén A",
        "notas": "Material triturado listo para envío"
    }
])

# Verificación: Mostrar el número de documentos en cada colección
print("Colecciones creadas con datos iniciales:")
print(f"Usuarios: {usuarios.count_documents({})} documentos")
print(f"Materiales: {materiales.count_documents({})} documentos")
print(f"Recolecciones: {recolecciones.count_documents({})} documentos")
print(f"Detalle_Recoleccion: {detalle_recoleccion.count_documents({})} documentos")
print(f"Procesos_Reciclaje: {procesos_reciclaje.count_documents({})} documentos")
print(f"Reportes: {reportes.count_documents({})} documentos")
print(f"Modelo_ML: {modelo_ml.count_documents({})} documentos")
print(f"Predicciones: {predicciones.count_documents({})} documentos")
print(f"Inventario: {inventario.count_documents({})} documentos")

# Cerrar la conexión
client.close()