# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # "patient", "doctor", "admin"

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # 👇 importante: este nombre lo usa tu código de seguridad
    hashed_password = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role    = relationship("Role", back_populates="users")

    patient = relationship("Patient", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)