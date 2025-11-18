# app/schemas/clinical_history.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClinicalHistoryBase(BaseModel):
    visit_date: datetime
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class ClinicalHistoryCreate(ClinicalHistoryBase):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None


class ClinicalHistoryUpdate(BaseModel):
    visit_date: Optional[datetime] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class ClinicalHistoryResponse(ClinicalHistoryBase):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
