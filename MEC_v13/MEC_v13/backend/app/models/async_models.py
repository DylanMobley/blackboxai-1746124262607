# app/async_models.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from datetime import datetime

# Load the asynchronous database URL from environment or use a default fallback
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

# Create an asynchronous engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,         # Database URL, with asyncpg driver for PostgreSQL
    echo=True,                   # Set to False in production to disable SQL logging
    pool_size=10,                # Connection pool size
    max_overflow=20,             # Extra connections beyond pool size during load
)

# Session factory for asynchronous sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,         # Use AsyncSession to support asynchronous queries
    expire_on_commit=False,      # Keeps objects from expiring automatically after commit
)

# Base class for defining SQLAlchemy models
Base = declarative_base()

# Example of a user model (you can extend with your other models)
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username}, email={self.email})>"

# Dependency to be used in FastAPI routes for getting async database session
async def get_async_db():
    async with AsyncSessionLocal() as session:  # Ensure session is properly closed after use
        yield session

# Add other models here (e.g., Persona, EmotionalState) as needed
class Persona(Base):
    __tablename__ = 'personas'

    persona_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    persona_name = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    energy_level = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="personas")

    def __repr__(self):
        return f"<Persona(id={self.persona_id}, name={self.persona_name}, tone={self.tone})>"

class EmotionalState(Base):
    __tablename__ = 'emotional_states'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    primary_emotion = Column(String, index=True)
    intensity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    needs = Column(JSON)
    function = Column(String)
    user_context = Column(String)

    user = relationship("User")

    def __repr__(self):
        return f"<EmotionalState(id={self.id}, primary_emotion={self.primary_emotion}, intensity={self.intensity})>"
