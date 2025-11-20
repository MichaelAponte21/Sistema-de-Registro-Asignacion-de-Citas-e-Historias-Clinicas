# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db.database import get_db
from app.core.db.models import User
from passlib.context import CryptContext



# Usamos pbkdf2_sha256 en lugar de bcrypt
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)


# --- Password hashing ---

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Endpoint donde se obtendrá el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# --- JWT helpers ---

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # jose devuelve normalmente str, lo convertimos a int
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario esté marcado como activo.
    """
    # Asumimos que User tiene is_active (lo comentaste en el modelo).
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user



def require_roles(allowed_roles: Sequence[str]) -> Callable:
    """
    Devuelve una dependencia que valida que el usuario tenga
    uno de los roles en allowed_roles por nombre.

    En este proyecto solo usaremos:
        - "admin"
        - "doctor"
        - "patient"
    """
    def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        role = getattr(current_user, "role", None)
        role_name = getattr(role, "name", None)

        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    role = getattr(current_user, "role", None)
    role_name = getattr(role, "name", None)

    if role_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only",
        )
    return current_user


def get_current_doctor_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    role = getattr(current_user, "role", None)
    role_name = getattr(role, "name", None)

    if role_name != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctors only",
        )
    return current_user


def get_current_patient_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    role = getattr(current_user, "role", None)
    role_name = getattr(role, "name", None)

    if role_name != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients only",
        )
    return current_user