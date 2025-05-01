# backend/services/persona_service.py

from sqlalchemy.orm import Session
from backend.models import Persona

def get_persona_by_user_id(db: Session, user_id: int):
    return db.query(Persona).filter(Persona.user_id == user_id).first()

def create_persona(db: Session, user_id: int, persona_name: str, tone: str, energy_level: str, goal: str):
    db_persona = Persona(
        user_id=user_id, 
        persona_name=persona_name, 
        tone=tone, 
        energy_level=energy_level, 
        goal=goal
    )
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def update_persona(db: Session, user_id: int, persona_name: str, tone: str, energy_level: str, goal: str):
    db_persona = db.query(Persona).filter(Persona.user_id == user_id).first()
    if db_persona:
        db_persona.persona_name = persona_name
        db_persona.tone = tone
        db_persona.energy_level = energy_level
        db_persona.goal = goal
        db.commit()
        db.refresh(db_persona)
        return db_persona
    return None

def delete_persona(db: Session, user_id: int):
    db_persona = db.query(Persona).filter(Persona.user_id == user_id).first()
    if db_persona:
        db.delete(db_persona)
        db.commit()
        return db_persona
    return None
