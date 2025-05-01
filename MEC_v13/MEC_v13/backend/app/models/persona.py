# models/persona.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Persona(Base):
    __tablename__ = "personas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    persona_name = Column(String)
    tone = Column(String)
    energy_level = Column(String)
    goal = Column(String)
    
    user = relationship("User", back_populates="personas")
