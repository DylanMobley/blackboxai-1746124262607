# backend/services/user_persona.py

from sqlalchemy.orm import Session
from backend.models import Persona, User  # Assuming you're using SQLAlchemy ORM models

def set_user_persona(user_id: str, persona_data: dict, db: Session):
    """
    Store user-specific persona information, including tone, goal, and energy level in the database.
    """
    persona = db.query(Persona).filter(Persona.user_id == user_id).first()
    
    if persona:
        # Update existing persona
        persona.persona_name = persona_data["persona"]
        persona.tone = persona_data["tone"]
        persona.energy_level = persona_data["energy_level"]
        persona.goal = persona_data["goal"]
        persona.updated_at = datetime.utcnow()
    else:
        # Create new persona if it doesn't exist
        persona = Persona(
            user_id=user_id,
            persona_name=persona_data["persona"],
            tone=persona_data["tone"],
            energy_level=persona_data["energy_level"],
            goal=persona_data["goal"],
            updated_at=datetime.utcnow()
        )
        db.add(persona)

    db.commit()

def get_user_persona(user_id: str, db: Session) -> dict:
    """
    Retrieve user-specific persona data from the database to ensure consistent persona behavior.
    """
    persona = db.query(Persona).filter(Persona.user_id == user_id).first()
    if persona:
        return {
            "persona": persona.persona_name,
            "tone": persona.tone,
            "energy_level": persona.energy_level,
            "goal": persona.goal
        }
    else:
        return None
