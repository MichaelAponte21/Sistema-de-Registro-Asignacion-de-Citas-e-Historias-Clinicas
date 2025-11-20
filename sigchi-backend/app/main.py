from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.core.db.database import Base, engine, SessionLocal
from app.core.db.models import User, Role
from app.core.security import get_password_hash
from app.routers import users, auth, patients, doctors, appointments, clinical_histories
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware

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
