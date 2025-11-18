from fastapi import FastAPI
from app.core.db.database import Base, engine
from app.routers import users, auth, patients, doctors, appointments, clinical_histories

# Esto asume que app.core.db.database ya importó app.models
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="SIGCHI Backend",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(auth.router)

app.include_router(patients.router)

app.include_router(doctors.router)

app.include_router(appointments.router)

app.include_router(clinical_histories.router)