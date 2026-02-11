# app/routers/patients.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import (
    require_roles,
    get_current_patient_user,
    get_current_active_user,
)
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
)
from app.services import patient_service


router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"],
)


# --- Crear paciente (solo admin o doctor) ---
@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "doctor"])),
):
    """
    Crea un perfil de paciente asociado a un usuario existente.
    Solo 'admin' y 'doctor' pueden crear pacientes.
    """

    # Evitar duplicados por user_id
    existing = patient_service.get_patient_by_user_id(db, patient_in.user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user already has a patient profile",
        )

    patient = patient_service.create_patient(db, patient_in)
    return patient


# --- Listar pacientes (solo admin; si quieres, puedes añadir 'doctor') ---
@router.get(
    "/",
    response_model=List[PatientResponse],
)
def list_patients(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "doctor"])),
):
    """
    Lista de pacientes con paginación básica.
    Admin y doctor.
    """
    patients = patient_service.list_patients(db, skip=skip, limit=limit)
    return patients


# --- Ver mi propio perfil de paciente (rol patient) ---
@router.get(
    "/me",
    response_model=PatientResponse,
)
def get_my_patient_profile(
    db: Session = Depends(get_db),
    current_patient_user: User = Depends(get_current_patient_user),
):
    """
    Devuelve el perfil de paciente asociado al usuario autenticado
    con rol 'patient'.
    """
    patient = patient_service.get_patient_by_user_id(db, current_patient_user.id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found for this user",
        )
    return patient


# --- Obtener paciente por id ---
@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
)
def get_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede ver cualquier paciente.
      - doctor: puede ver cualquier paciente (más adelante podemos filtrar 'sus' pacientes).
      - patient: solo puede ver su propio registro.
    """
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    role = getattr(current_user, "role", None)
    role_name = getattr(role, "name", None)

    if role_name == "patient":
        # El paciente solo se puede ver a sí mismo
        if patient.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access another patient's data",
            )

    elif role_name in ("admin", "doctor"):
        # Por ahora, admin/doctor pueden ver cualquier paciente.
        # Más adelante, podemos restringir doctor a "sus" pacientes.
        pass

    else:
        # Rol desconocido (por si acaso)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return patient


# --- Actualizar paciente (solo admin o doctor) ---
@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
)
def update_patient(
    patient_id: int,
    patient_in: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "doctor"])),
):
    """
    Actualiza datos de un paciente.
    Solo 'admin' o 'doctor'.
    (En el futuro podemos agregar lógica para que el doctor solo
    pueda modificar sus propios pacientes).
    """
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    patient = patient_service.update_patient(db, patient, patient_in)
    return patient


# --- Eliminar paciente (solo admin) ---
@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    """
    Elimina un paciente (delete físico).
    Solo 'admin'. Más adelante podrías cambiarlo a soft-delete.
    """
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    patient_service.delete_patient(db, patient)
    return None
