# app/routers/appointments.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import (
    get_current_active_user,
)
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from app.services import (
    appointment_service,
    patient_service,
    doctor_service,
)


router = APIRouter(
    prefix="/api/appointments",
    tags=["Appointments"],
)


def _get_role_name(current_user: User) -> str | None:
    role = getattr(current_user, "role", None)
    return getattr(role, "name", None)


def _get_current_patient_id_for_user(db: Session, current_user: User) -> int | None:
    patient = patient_service.get_patient_by_user_id(db, current_user.id)
    return patient.id if patient else None


def _get_current_doctor_id_for_user(db: Session, current_user: User) -> int | None:
    doctor = doctor_service.get_doctor_by_user_id(db, current_user.id)
    return doctor.id if doctor else None


# --- Crear cita ---
@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - 'admin': puede crear citas para cualquier paciente/doctor válidos.
      - 'doctor': solo puede crear citas donde doctor_id sea su propio perfil.
      - 'patient': solo puede crear citas donde patient_id sea su propio perfil.
    """
    role_name = _get_role_name(current_user)

    # Validar existencia de patient y doctor
    patient = patient_service.get_patient(db, appointment_in.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient_id",
        )

    doctor = doctor_service.get_doctor(db, appointment_in.doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid doctor_id",
        )

    if role_name == "admin":
        # Admin puede crear cualquier cita válida
        pass

    elif role_name == "doctor":
        current_doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not current_doctor_id or current_doctor_id != appointment_in.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Doctors can only create appointments for themselves",
            )

    elif role_name == "patient":
        current_patient_id = _get_current_patient_id_for_user(db, current_user)
        if not current_patient_id or current_patient_id != appointment_in.patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Patients can only create appointments for themselves",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    appointment = appointment_service.create_appointment(db, appointment_in)
    return appointment


# --- Listar citas ---
@router.get(
    "/",
    response_model=List[AppointmentResponse],
)
def list_appointments(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: ve todas las citas.
      - doctor: ve solo sus citas (doctor_id propio).
      - patient: ve solo sus citas (patient_id propio).
    """
    role_name = _get_role_name(current_user)

    if role_name == "admin":
        return appointment_service.list_appointments(db, skip=skip, limit=limit)

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor profile not found for this user",
            )
        return appointment_service.list_appointments_by_doctor(
            db, doctor_id=doctor_id, skip=skip, limit=limit
        )

    elif role_name == "patient":
        patient_id = _get_current_patient_id_for_user(db, current_user)
        if not patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient profile not found for this user",
            )
        return appointment_service.list_appointments_by_patient(
            db, patient_id=patient_id, skip=skip, limit=limit
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


# --- Obtener cita por id ---
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede ver cualquier cita.
      - doctor: solo citas donde él sea el doctor.
      - patient: solo citas donde él sea el paciente.
    """
    appointment = appointment_service.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        return appointment

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id or doctor_id != appointment.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own appointments",
            )
        return appointment

    elif role_name == "patient":
        patient_id = _get_current_patient_id_for_user(db, current_user)
        if not patient_id or patient_id != appointment.patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own appointments",
            )
        return appointment

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


# --- Actualizar cita (admin o doctor dueño) ---
@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede actualizar cualquier cita.
      - doctor: solo citas donde él sea el doctor.
      - patient: no actualiza (solo puede cancelar desde el endpoint de cancelación).
    """
    appointment = appointment_service.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        pass

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id or doctor_id != appointment.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own appointments",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or doctors can update appointments",
        )

    appointment = appointment_service.update_appointment(db, appointment, appointment_in)
    return appointment


# --- Cancelar cita ---
@router.post(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse,
)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede cancelar cualquier cita.
      - doctor: solo citas donde él sea el doctor.
      - patient: solo citas donde él sea el paciente.
    """
    appointment = appointment_service.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        pass

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id or doctor_id != appointment.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own appointments",
            )

    elif role_name == "patient":
        patient_id = _get_current_patient_id_for_user(db, current_user)
        if not patient_id or patient_id != appointment.patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own appointments",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    appointment = appointment_service.set_appointment_status(db, appointment, "cancelled")
    return appointment
