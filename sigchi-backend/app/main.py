from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from sqlalchemy.orm import Session
from app.core.db.database import Base, engine, SessionLocal
from app.core.db.models import User, Role
from app.core.security import get_password_hash
from app.core.config import settings
from app.routers import users, auth, patients, doctors, appointments, clinical_histories
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware

# Rutas del frontend estatico
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
LOGIN_FILE = FRONTEND_DIR / "login.html"
ADMIN_FILE = FRONTEND_DIR / "admin.html"
DOCTOR_FILE = FRONTEND_DIR / "doctor.html"
PATIENT_FILE = FRONTEND_DIR / "patient.html"

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGCHI Backend",
    version="0.1.0",
)

# Permitir solicitudes CORS desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite cualquier método HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite cualquier encabezado
)

# Servir archivos estaticos del frontend
app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

# --- Middleware de autenticacion para vistas HTML ---

PROTECTED_HTML = {
    "/admin": ["admin"],
    "/doctor": ["doctor"],
    "/patient": ["patient"],
}


def extract_token(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header.split(" ", 1)[1]
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    return None


def resolve_user(token: str) -> tuple[User, str]:
    """
    Decodifica el token JWT y recupera el usuario y su rol.
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    user_id = payload.get("sub")
    if user_id is None:
        raise JWTError("Token sin sub")
    user_id = int(user_id)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise JWTError("Usuario no encontrado")
        role = getattr(user, "role", None)
        role_name = getattr(role, "name", None)
        return user, role_name
    finally:
        db.close()


class AuthHTMLMiddleware(BaseHTTPMiddleware):
    """
    Protege las rutas HTML por rol. Usa el token (header Authorization o cookie access_token)
    y redirige a /login si falta o no cumple el rol.
    """
    async def dispatch(self, request: Request, call_next):
        path = request.url.path.rstrip("/") or "/"

        # No proteger rutas de API ni estaticos ni docs
        if path.startswith("/api") or path.startswith("/frontend") or path.startswith("/docs") or path.startswith("/openapi") or path.startswith("/redoc"):
            return await call_next(request)

        # rutas publicas
        if path in {"/", "/login"}:
            return await call_next(request)

        allowed_roles = PROTECTED_HTML.get(path)
        if allowed_roles:
            token = extract_token(request)
            if not token:
                return RedirectResponse(url="/login", status_code=302)
            try:
                user, role_name = resolve_user(token)
            except JWTError:
                return RedirectResponse(url="/login", status_code=302)

            if role_name not in allowed_roles:
                return RedirectResponse(url="/login", status_code=302)
            request.state.user = user
            request.state.role_name = role_name

        return await call_next(request)


app.add_middleware(AuthHTMLMiddleware)


# Rutas HTML por modulo
@app.get("/", include_in_schema=False)
async def serve_root():
    return RedirectResponse(url="/login")


@app.get("/login", include_in_schema=False)
async def serve_login():
    return FileResponse(LOGIN_FILE)


@app.get("/admin", include_in_schema=False)
async def serve_admin():
    return FileResponse(ADMIN_FILE)


@app.get("/doctor", include_in_schema=False)
async def serve_doctor():
    return FileResponse(DOCTOR_FILE)


@app.get("/patient", include_in_schema=False)
async def serve_patient():
    return FileResponse(PATIENT_FILE)


@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    """
    Favicon placeholder to evitar 404 en navegadores.
    """
    return Response(status_code=204)


# Función para crear el rol de admin si no existe
def create_admin_role(db: Session):
    # Verificar si el rol 'admin' ya existe
    admin_role = db.query(Role).filter(Role.name == "admin").first()

    if not admin_role:
        # Si no existe, crear el rol 'admin'
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        print("Rol admin creado")
    else:
        print("El rol admin ya existe")


# Función para crear el usuario admin si no existe
def create_admin_user(db: Session):
    # Verificar si el usuario admin ya existe
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()

    if not admin_user:
        # Crear el usuario admin siguiendo la estructura esperada por el endpoint
        admin_role = db.query(Role).filter(Role.name == "admin").first()

        # La contraseña se pasa en texto plano, y luego se genera el hash
        hashed_password = get_password_hash("admin_password")

        # Crear el nuevo usuario admin
        admin_user = User(
            email="admin@example.com",
            hashed_password=hashed_password,
            first_name="Admin",
            last_name="User",
            is_active=True,
            role_id=admin_role.id  # Asignar el ID del rol admin
        )

        db.add(admin_user)
        db.commit()
        print("Usuario admin creado")
    else:
        print("El usuario admin ya existe")


# Llamar a las funciones de inicialización al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    db: Session = SessionLocal()  # Obtener la sesión de la base de datos
    create_admin_role(db)  # Crear el rol admin si no existe
    create_admin_user(db)  # Crear el usuario admin si no existe

origins = [
    "http://localhost:3000",  # Dirección de tu frontend
    "http://localhost",       # Para localhost también
    "http://localhost:8000",  # Para probar localmente
]

origins = [
    "http://localhost:3000",  # Dirección de tu frontend
    "http://localhost",       # Para localhost también
    "http://localhost:8000",  # Para probar localmente
]

# Incluir los routers


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(clinical_histories.router)
