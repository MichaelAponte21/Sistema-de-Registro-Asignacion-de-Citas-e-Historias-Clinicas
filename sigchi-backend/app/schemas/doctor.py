# app/schemas/doctor.py

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    specialty: Optional[str] = None


class DoctorCreate(DoctorBase):
    user_id: int


class DoctorUpdate(DoctorBase):
    # Todos los campos son opcionales (heredados) → sirve para PUT/PATCH
    pass


class DoctorResponse(DoctorBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
