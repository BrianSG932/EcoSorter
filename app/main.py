#main.py

from fastapi import FastAPI
from app.routes import clasificador

app = FastAPI(
    title="EcoSorter API",
    description="Clasificación de residuos usando CNN",
    version="1.0.0"
)

# Registrar las rutas
app.include_router(clasificador.router)

# Ruta principal
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de EcoSorter"}