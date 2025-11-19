# app/models/patient.py

from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    # Relación 1:1 con User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Datos del paciente
    document_type = Column(String(10), nullable=True)      # CC, TI, etc.
    document_number = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)

    # Relación inversa hacia User
    user = relationship("User", back_populates="patient")
