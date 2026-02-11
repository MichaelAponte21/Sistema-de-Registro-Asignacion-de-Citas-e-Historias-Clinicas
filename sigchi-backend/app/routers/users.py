# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.db.database import get_db
from app.core.db.models import User, Role
from app.core.security import (
    get_password_hash,
    get_current_user,
    get_current_admin_user,
)
from app.schemas.user import UserCreate, UserResponse
from fastapi import Body


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    # 1) ¿Ya existe un usuario con ese email?
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 2) ¿El role_id es válido?
    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role_id",
        )

    # 3) Crear el usuario
    db_user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role_id=payload.role_id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Listado de usuarios, solo para admin.
    """
    users = (
        db.query(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
