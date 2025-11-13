from fastapi import FastAPI

from app.db.database import Base, engine
from app.db import models
from app.routers import health, patients

# Crear tablas en la BD al iniciar (solo en desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGCHI - Sistema de Gestión de Citas e Historias Clínicas",
    version="0.1.0"
)

app.include_router(health.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
