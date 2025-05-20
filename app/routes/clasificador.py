#clasificador.py api
from fastapi import APIRouter, UploadFile, File
from app.services.modelo_ml import cargar_modelo_y_clases, predecir_imagen
import shutil
from app.db.conexion_mongo import get_db
import os
from datetime import datetime

router = APIRouter(prefix="/clasificador", tags=["Clasificador"])

modelo, clases = cargar_modelo_y_clases()

@router.post("/predecir")
async def predecir(file: UploadFile = File(...)):
    # Guardar temporalmente el archivo
    ruta_temp = f"temp_{file.filename}"
    with open(ruta_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Predecir
    resultado = predecir_imagen(ruta_temp, modelo, clases)

    
    # Eliminar el archivo temporal para mantener limpio el entorno
    os.remove(ruta_temp)

    # Agregar la fecha de predicción
    resultado["fecha_prediccion"] = datetime.now()

    # Insertar el resultado en la colección "Predicciones"
    db, client = get_db()
    predicciones = db['Predicciones']

    pred_doc = {
        "fecha_prediccion": resultado["fecha_prediccion"],
        "resultado": resultado["material"],
        "precision": resultado["confianza"],
        "entrada": file.filename  # Puedes agregar más detalles de la entrada si lo deseas
    }

    insert_result = predicciones.insert_one(pred_doc)
    prediction_id = str(insert_result.inserted_id)

    client.close()  # Cerramos la conexión a la BD
    
    return {"clase_predicha": resultado, "prediccion_id": prediction_id}