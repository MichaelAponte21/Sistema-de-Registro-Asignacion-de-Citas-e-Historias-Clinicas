# app/services/appointment_service.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Appointment


def create_appointment(db: Session, appointment_in) -> Appointment:
    appointment = Appointment(
        patient_id=appointment_in.patient_id,
        doctor_id=appointment_in.doctor_id,
        scheduled_at=appointment_in.scheduled_at,
        reason=appointment_in.reason,
        notes=appointment_in.notes,
        status="scheduled",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def list_appointments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> List[Appointment]:
    return db.query(Appointment).offset(skip).limit(limit).all()


def list_appointments_by_doctor(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 20,
) -> List[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_appointments_by_patient(
    db: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 20,
) -> List[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_appointment(
    db: Session,
    appointment: Appointment,
    appointment_in,
) -> Appointment:
    data = appointment_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(appointment, field, value)

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def set_appointment_status(
    db: Session,
    appointment: Appointment,
    status_value: str,
) -> Appointment:
    appointment.status = status_value
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
