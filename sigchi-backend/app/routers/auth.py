# app/routers/auth.py

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.core.config import settings


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """
    Devuelve el usuario si las credenciales son válidas,
    o None si son inválidas.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Endpoint de login para OAuth2 "password flow".

    Recibe:
      - username: email del usuario
      - password: contraseña en texto plano

    Devuelve:
      - access_token: JWT con sub = user.id
      - token_type: "bearer"
    """

    # En nuestro sistema, username == email
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Opcional: podrías bloquear usuarios inactivos aquí también
    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Muy importante: sub debe ser un str con el id del usuario,
    # porque get_current_user luego hace int(sub)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "role": user.role.name,
    }
