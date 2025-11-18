# app/schemas/patient.py

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    document_type: Optional[str] = None      # CC, TI, etc.
    document_number: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None


class PatientCreate(PatientBase):
    # Asociamos el paciente a un usuario ya existente
    user_id: int


class PatientUpdate(PatientBase):
    # Todos opcionales; se usa para updates parciales o completos
    pass


class PatientResponse(PatientBase):
    id: int
    user_id: int

    # Si quieres exponer algo del User asociado:
    # email: Optional[str] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
