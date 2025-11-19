# app/schemas/appointment.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    scheduled_at: datetime
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int
    # El status siempre empieza en "scheduled" desde backend,
    # no lo exponemos aquí (lo fijamos en el servicio).


class AppointmentUpdate(BaseModel):
    """
    Update genérico para admin/doctor.
    No obligamos a enviar todos los campos.
    """
    scheduled_at: Optional[datetime] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None  # "scheduled", "completed", "cancelled", etc.


class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
