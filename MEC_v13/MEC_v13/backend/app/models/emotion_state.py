# models/emotion_state.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from . import Base
from datetime import datetime

class EmotionState(Base):
    __tablename__ = "emotion_states"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    primary_emotion = Column(String)
    intensity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    needs = Column(JSON)  # A list of unmet needs in JSON format
    function = Column(String)
    
    user = relationship("User", back_populates="emotion_states")
