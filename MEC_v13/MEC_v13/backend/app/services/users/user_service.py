# backend/services/user_service.py

from sqlalchemy.orm import Session
from backend.models import User
from backend.database import get_db

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    db_user = User(username=username, email=email, password=password)  # Make sure to hash the password in a real-world scenario
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, username: str, email: str, password: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db_user.username = username
        db_user.email = email
        db_user.password = password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
