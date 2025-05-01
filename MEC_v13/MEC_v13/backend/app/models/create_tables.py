# backend/create_tables.py

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.models import Base  # Import the Base from models
import os
import asyncio

# Load async database URL from environment
DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create sessionmaker for async operations
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Asynchronous function to create all tables
async def create_tables():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

    print("Tables created successfully.")

# Run the table creation asynchronously
if __name__ == "__main__":
    asyncio.run(create_tables())
