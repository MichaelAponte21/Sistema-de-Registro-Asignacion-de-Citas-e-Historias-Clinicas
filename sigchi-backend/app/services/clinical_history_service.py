# app/services/clinical_history_service.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import ClinicalHistory


def create_history(
    db: Session,
    history_in,
) -> ClinicalHistory:
    history = ClinicalHistory(
        patient_id=history_in.patient_id,
        doctor_id=history_in.doctor_id,
        appointment_id=history_in.appointment_id,
        visit_date=history_in.visit_date,
        diagnosis=history_in.diagnosis,
        treatment=history_in.treatment,
        notes=history_in.notes,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_history(
    db: Session,
    history_id: int,
) -> Optional[ClinicalHistory]:
    return db.query(ClinicalHistory).filter(ClinicalHistory.id == history_id).first()


def list_histories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> List[ClinicalHistory]:
    return db.query(ClinicalHistory).offset(skip).limit(limit).all()


def list_histories_by_patient(
    db: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 50,
) -> List[ClinicalHistory]:
    return (
        db.query(ClinicalHistory)
        .filter(ClinicalHistory.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_histories_by_doctor(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 50,
) -> List[ClinicalHistory]:
    return (
        db.query(ClinicalHistory)
        .filter(ClinicalHistory.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_history(
    db: Session,
    history: ClinicalHistory,
    history_in,
) -> ClinicalHistory:
    data = history_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(history, field, value)

    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def delete_history(
    db: Session,
    history: ClinicalHistory,
) -> None:
    db.delete(history)
    db.commit()
