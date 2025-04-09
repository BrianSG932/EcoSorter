from fastapi import APIRouter, File, UploadFile
from app.services.modelo_ml import predecir_residuo

router = APIRouter()

@router.post("/clasificar")
async def clasificar_residuo(imagen: UploadFile = File(...)):
    resultado = await predecir_residuo(imagen)
    return resultado
