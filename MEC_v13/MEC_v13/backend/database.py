# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .database_config import DATABASE_URL  # Ensure DATABASE_URL is correctly loaded from your environment

# Create an engine with connection pooling
# `pool_size`: The number of connections to keep in the pool
# `max_overflow`: The maximum number of connections to allow beyond `pool_size`
# `pool_timeout`: How long to wait for a connection before timing out
engine = create_engine(
    DATABASE_URL, 
    poolclass=QueuePool,  # Use QueuePool for connection pooling
    pool_size=10,         # Pool size (number of connections to keep open)
    max_overflow=20,      # Allow up to 20 extra connections beyond the pool size
    pool_timeout=30,      # Timeout (seconds) to wait for a connection from the pool
)

# SessionLocal is the session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency function to get the current database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables (called once on app startup)
def create_db():
    """Create all database tables using SQLAlchemy models."""
    from backend.models import Base  # Import Base from models
    Base.metadata.create_all(bind=engine)
