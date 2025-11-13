from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional


class PatientBase(BaseModel):
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    personal_history: Optional[str] = None
    family_history: Optional[str] = None


class PatientCreate(PatientBase):
    username: str
    password: str
    full_name: str
    document_type: str
    document_number: str
    email: EmailStr
    phone: Optional[str] = None


class PatientUpdate(PatientBase):
    pass


class PatientUserInfo(BaseModel):
    id: int
    full_name: str
    document_type: str
    document_number: str
    email: EmailStr
    phone: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2


class PatientOut(PatientBase):
    id: int
    user: PatientUserInfo

    class Config:
        from_attributes = True
