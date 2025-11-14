from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import get_db
from app.db import models
from app.db.models import UserRole
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    if password is None:
        raise ValueError("Password is required")

    safe_password = password[:72]  # por si acaso
    return pwd_context.hash(safe_password)


@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    # Validar duplicados: username, documento, email
    existing_user = db.query(models.User).filter(
        (models.User.username == payload.username) |
        (models.User.document_number == payload.document_number) |
        (models.User.email == payload.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese username, documento o email."
        )

    user = models.User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        full_name=payload.full_name,
        document_type=payload.document_type,
        document_number=payload.document_number,
        email=payload.email,
        phone=payload.phone,
        role=UserRole.PATIENT,
        active=True
    )

    db.add(user)
    db.flush()  # para obtener user.id sin hacer commit aún

    patient = models.Patient(
        user_id=user.id,
        birth_date=payload.birth_date,
        sex=payload.sex,
        address=payload.address,
        emergency_contact=payload.emergency_contact,
        personal_history=payload.personal_history,
        family_history=payload.family_history,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


@router.get("/", response_model=List[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Actualizar solo los campos enviados
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    db.delete(patient)
    db.commit()
    return
