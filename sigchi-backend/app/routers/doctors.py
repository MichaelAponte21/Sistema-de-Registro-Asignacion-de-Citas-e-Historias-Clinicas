# app/routers/doctors.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import (
    require_roles,
    get_current_admin_user,
    get_current_doctor_user,
    get_current_active_user,
)
from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
)
from app.services import doctor_service
from app.core.db.models import Doctor


router = APIRouter(
    prefix="/api/doctors",
    tags=["Doctors"],
)

def doctor_to_response(doctor: Doctor) -> dict:
    user = getattr(doctor, "user", None)
    email = getattr(user, "email", None)
    return {
        "id": doctor.id,
        "user_id": doctor.user_id,
        "specialty": doctor.specialty,
        "user_email": email,
    }


# --- Crear doctor (solo admin) ---
@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(
    doctor_in: DoctorCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Crea un perfil de doctor asociado a un usuario existente.
    Reglas:
      - Solo 'admin' puede crear doctores.
      - El usuario referenciado debe tener rol 'doctor'.
      - No debe existir ya un perfil de doctor para ese user_id.
    """

    # ¿Ya existe un perfil de doctor para ese usuario?
    existing = doctor_service.get_doctor_by_user_id(db, doctor_in.user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user already has a doctor profile",
        )

    # Validar que el usuario existe
    user = db.query(User).filter(User.id == doctor_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    # Validar que su rol sea 'doctor'
    role = getattr(user, "role", None)
    role_name = getattr(role, "name", None)
    if role_name != "doctor":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have role 'doctor' to create a doctor profile",
        )

    doctor = doctor_service.create_doctor(db, doctor_in)
    return doctor_to_response(doctor)


# --- Listar doctores (solo admin; si quieres, agregar 'doctor') ---
@router.get(
    "/",
    response_model=List[DoctorResponse],
)
def list_doctors(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    """
    Lista doctores con paginación básica.
    Solo 'admin' (puedes añadir 'doctor' en require_roles si lo necesitas).
    """
    doctors = doctor_service.list_doctors(db, skip=skip, limit=limit)
    return [doctor_to_response(d) for d in doctors]


# --- Ver mi perfil de doctor (rol doctor) ---
@router.get(
    "/me",
    response_model=DoctorResponse,
)
def get_my_doctor_profile(
    db: Session = Depends(get_db),
    current_doctor_user: User = Depends(get_current_doctor_user),
):
    """
    Devuelve el perfil de doctor asociado al usuario autenticado
    con rol 'doctor'.
    """
    doctor = doctor_service.get_doctor_by_user_id(db, current_doctor_user.id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found for this user",
        )
    return doctor_to_response(doctor)


# --- Obtener doctor por id (visible para cualquier usuario activo) ---
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    En este punto, la información del doctor la consideramos "pública"
    (sirve para que pacientes vean con quién pueden agendar).
    Si luego quieres limitar, puedes añadir lógica por rol aquí.
    """
    doctor = doctor_service.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return doctor_to_response(doctor)


# --- Actualizar doctor (admin o el propio doctor) ---
@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def update_doctor(
    doctor_id: int,
    doctor_in: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Actualiza datos de un doctor.
    Reglas:
      - admin: puede actualizar cualquier doctor.
      - doctor: solo su propio perfil.
    """
    doctor = doctor_service.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    role = getattr(current_user, "role", None)
    role_name = getattr(role, "name", None)

    if role_name == "admin":
        # Admin puede actualizar cualquiera
        pass
    elif role_name == "doctor":
        # El doctor solo puede actualizar su propio perfil
        if doctor.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own doctor profile",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    doctor = doctor_service.update_doctor(db, doctor, doctor_in)
    return doctor_to_response(doctor)


# --- Eliminar doctor (solo admin) ---
@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Elimina un doctor (delete físico).
    Solo 'admin'. Más adelante podrías cambiarlo a soft-delete.
    """
    doctor = doctor_service.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    doctor_service.delete_doctor(db, doctor)
    return None
