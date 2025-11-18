# app/routers/clinical_histories.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import get_current_active_user
from app.schemas.clinical_history import (
    ClinicalHistoryCreate,
    ClinicalHistoryUpdate,
    ClinicalHistoryResponse,
)
from app.services import (
    clinical_history_service,
    patient_service,
    doctor_service,
)


router = APIRouter(
    prefix="/api/histories",
    tags=["Clinical Histories"],
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


# --- Crear historia clínica ---
@router.post(
    "/",
    response_model=ClinicalHistoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_clinical_history(
    history_in: ClinicalHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede crear historias para cualquier combinación paciente/doctor válida.
      - doctor: solo puede crear historias donde doctor_id corresponda a su propio perfil.
      - patient: NO puede crear historias.
    """
    role_name = _get_role_name(current_user)

    # Validar existencia de patient y doctor
    patient = patient_service.get_patient(db, history_in.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient_id",
        )

    doctor = doctor_service.get_doctor(db, history_in.doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid doctor_id",
        )

    if role_name == "admin":
        pass

    elif role_name == "doctor":
        current_doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not current_doctor_id or current_doctor_id != history_in.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Doctors can only create histories for themselves as doctor",
            )

    else:
        # patients (y cualquier rol no esperado) no pueden crear
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or doctors can create clinical histories",
        )

    history = clinical_history_service.create_history(db, history_in)
    return history


# --- Listar historias según rol ---
@router.get(
    "/",
    response_model=List[ClinicalHistoryResponse],
)
def list_clinical_histories(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: ve todas las historias.
      - doctor: ve solo historias donde él sea el doctor.
      - patient: ve solo historias donde él sea el paciente.
    """
    role_name = _get_role_name(current_user)

    if role_name == "admin":
        return clinical_history_service.list_histories(db, skip=skip, limit=limit)

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor profile not found for this user",
            )
        return clinical_history_service.list_histories_by_doctor(
            db, doctor_id=doctor_id, skip=skip, limit=limit
        )

    elif role_name == "patient":
        patient_id = _get_current_patient_id_for_user(db, current_user)
        if not patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient profile not found for this user",
            )
        return clinical_history_service.list_histories_by_patient(
            db, patient_id=patient_id, skip=skip, limit=limit
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


# --- Ver historia por id ---
@router.get(
    "/{history_id}",
    response_model=ClinicalHistoryResponse,
)
def get_clinical_history_by_id(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede ver cualquier historia.
      - doctor: solo historias donde él sea el doctor.
      - patient: solo historias donde él sea el paciente.
    """
    history = clinical_history_service.get_history(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinical history not found",
        )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        return history

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id or doctor_id != history.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access histories where you are the doctor",
            )
        return history

    elif role_name == "patient":
        patient_id = _get_current_patient_id_for_user(db, current_user)
        if not patient_id or patient_id != history.patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own clinical histories",
            )
        return history

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


# --- Listar historias de un paciente específico (admin/doctor/patient) ---
@router.get(
    "/patient/{patient_id}",
    response_model=List[ClinicalHistoryResponse],
)
def list_histories_for_patient(
    patient_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede ver historias de cualquier paciente.
      - doctor: solo historias donde él sea el doctor del paciente indicado.
      - patient: solo puede usar este endpoint si patient_id corresponde a su propio perfil.
    """
    history_list = clinical_history_service.list_histories_by_patient(
        db, patient_id=patient_id, skip=skip, limit=limit
    )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        return history_list

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor profile not found for this user",
            )
        # Verificamos que todas las historias devueltas sean de él
        for history in history_list:
            if history.doctor_id != doctor_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only see histories where you are the doctor",
                )
        return history_list

    elif role_name == "patient":
        current_patient_id = _get_current_patient_id_for_user(db, current_user)
        if not current_patient_id or current_patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only see your own clinical histories",
            )
        return history_list

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


# --- Actualizar historia (admin o doctor dueño) ---
@router.put(
    "/{history_id}",
    response_model=ClinicalHistoryResponse,
)
def update_clinical_history(
    history_id: int,
    history_in: ClinicalHistoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reglas:
      - admin: puede actualizar cualquier historia.
      - doctor: solo historias donde él sea el doctor.
      - patient: no puede actualizar.
    """
    history = clinical_history_service.get_history(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinical history not found",
        )

    role_name = _get_role_name(current_user)

    if role_name == "admin":
        pass

    elif role_name == "doctor":
        doctor_id = _get_current_doctor_id_for_user(db, current_user)
        if not doctor_id or doctor_id != history.doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update histories where you are the doctor",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or doctors can update clinical histories",
        )

    history = clinical_history_service.update_history(db, history, history_in)
    return history


# --- Eliminar historia (solo admin) ---
@router.delete(
    "/{history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_clinical_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Elimina una historia clínica (borrado físico).
    Solo 'admin'.
    """
    role_name = _get_role_name(current_user)
    if role_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete clinical histories",
        )

    history = clinical_history_service.get_history(db, history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinical history not found",
        )

    clinical_history_service.delete_history(db, history)
    return None
