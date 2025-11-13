# app/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    ADMIN_SYSTEM = "ADMIN_SYSTEM"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    document_type = Column(String(20), nullable=False)
    document_number = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    role = Column(Enum(UserRole), nullable=False)
    active = Column(Boolean, default=True)

    patient = relationship("Patient", back_populates="user", uselist=False)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    sex = Column(String(10), nullable=True)
    address = Column(String(255), nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    personal_history = Column(Text, nullable=True)
    family_history = Column(Text, nullable=True)

    user = relationship("User", back_populates="patient")
