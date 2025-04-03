from fastapi import FastAPI
from app.routes import clasificador

app = FastAPI(title="EcoSorter API")

app.include_router(clasificador.router)