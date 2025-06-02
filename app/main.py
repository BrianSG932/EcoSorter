#main.py api

from fastapi import FastAPI
from app.routes import clasificador
from app.routes import auth_google
from app.routes import auth_register

app = FastAPI(
    title="EcoSorter API",
    description="Clasificación de residuos usando CNN",
    version="1.0.0"
)

# Registrar las rutas
app.include_router(clasificador.router)

app.include_router(auth_google.router)

app.include_router(auth_register.router)

# Ruta principal
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de EcoSorter"}