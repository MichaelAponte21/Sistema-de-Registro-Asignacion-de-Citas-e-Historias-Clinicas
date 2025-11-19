from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def create_user(db: Session, data):
    hashed_pw = hash_password(data.password)

    new_user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hashed_pw,
        role_id=data.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
