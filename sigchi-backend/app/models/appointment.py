# app/models/appointment.py

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.db.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    # Cuándo es la cita
    scheduled_at = Column(DateTime(timezone=True), nullable=False)

    # Estados típicos: "scheduled", "completed", "cancelled"
    status = Column(String(20), nullable=False, default="scheduled")

    # Motivo de la consulta (texto corto) y notas internas (texto más largo)
    reason = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    patient = relationship("Patient", backref="appointments")
    doctor = relationship("Doctor", backref="appointments")
