from fastapi import APIRouter, UploadFile, File
from app.services.modelo_ml import predecir_residuo

router = APIRouter(prefix="/api", tags=["Clasificador"])

@router.post("/clasificar")
async def clasificar_residuo(imagen: UploadFile = File(...)):
    resultado = await predecir_residuo(imagen)
    return resultado