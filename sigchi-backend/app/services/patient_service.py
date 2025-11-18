# app/services/patient_service.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def create_patient(db: Session, patient_in: PatientCreate) -> Patient:
    patient = Patient(
        user_id=patient_in.user_id,
        document_type=patient_in.document_type,
        document_number=patient_in.document_number,
        phone=patient_in.phone,
        address=patient_in.address,
        birth_date=patient_in.birth_date,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_user_id(db: Session, user_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def list_patients(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()


def update_patient(
    db: Session,
    patient: Patient,
    patient_in: PatientUpdate,
) -> Patient:
    data = patient_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(patient, field, value)

    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient: Patient) -> None:
    db.delete(patient)
    db.commit()
