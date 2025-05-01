# backend/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base  # Assuming you have a Base class for SQLAlchemy models

# User Model to store basic user information
class User(Base):
    """ User model to store basic user information """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Storing password (hashed in real-world scenarios)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    personas = relationship("Persona", back_populates="user")
    emotion_history = relationship("EmotionHistory", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username}, email={self.email})>"

# Persona Model to store persona data for users
class Persona(Base):
    """ Persona model to store persona data for users """
    __tablename__ = 'personas'

    persona_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    persona_name = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    energy_level = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="personas")

    def __repr__(self):
        return f"<Persona(id={self.persona_id}, name={self.persona_name}, tone={self.tone}, energy_level={self.energy_level})>"

# EmotionHistory Model to track emotional states over time
class EmotionHistory(Base):
    """ Emotion History model to track emotional states over time """
    __tablename__ = 'emotion_history'

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    emotion = Column(String, nullable=False)
    intensity = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="emotion_history")

    def __repr__(self):
        return f"<EmotionHistory(id={self.history_id}, emotion={self.emotion}, intensity={self.intensity}, timestamp={self.timestamp})>"

# EmotionalState Model to store specific emotional states of the user
class EmotionalState(Base):
    """ EmotionalState model to store specific emotional states of the user """
    __tablename__ = 'emotional_states'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)  # Foreign Key for User
    primary_emotion = Column(String, index=True)
    intensity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    needs = Column(JSON)  # List of unmet needs as JSON
    function = Column(String)
    user_context = Column(String)  # Additional user context (optional)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<EmotionalState(id={self.id}, primary_emotion={self.primary_emotion}, intensity={self.intensity}, timestamp={self.timestamp})>"
