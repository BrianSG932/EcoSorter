from fastapi import FastAPI
from app.routes import residuos  # o el nombre real de tu archivo en /routes/

app = FastAPI(title="EcoSorter API")

app.include_router(residuos.router)