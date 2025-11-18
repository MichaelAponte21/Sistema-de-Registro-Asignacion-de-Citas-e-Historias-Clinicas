# app/models/clinical_history.py

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db.database import Base


class ClinicalHistory(Base):
    __tablename__ = "clinical_histories"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    # Opcional, para enlazar con una cita específica (si existe)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)

    # Información clínica
    visit_date = Column(DateTime(timezone=True), nullable=False)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
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

    patient = relationship("Patient", backref="clinical_histories")
    doctor = relationship("Doctor", backref="clinical_histories")
    appointment = relationship("Appointment", backref="clinical_history", uselist=False)

