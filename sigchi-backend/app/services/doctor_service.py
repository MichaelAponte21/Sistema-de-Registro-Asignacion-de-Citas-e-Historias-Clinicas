# app/services/doctor_service.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate


def create_doctor(db: Session, doctor_in: DoctorCreate) -> Doctor:
    doctor = Doctor(
        user_id=doctor_in.user_id,
        specialty=doctor_in.specialty,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor(db: Session, doctor_id: int) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctor_by_user_id(db: Session, user_id: int) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.user_id == user_id).first()


def list_doctors(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> List[Doctor]:
    return db.query(Doctor).offset(skip).limit(limit).all()


def update_doctor(
    db: Session,
    doctor: Doctor,
    doctor_in: DoctorUpdate,
) -> Doctor:
    data = doctor_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(doctor, field, value)

    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor: Doctor) -> None:
    db.delete(doctor)
    db.commit()
