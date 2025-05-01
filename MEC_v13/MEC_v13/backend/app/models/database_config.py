# database_config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if available)
load_dotenv()

# Get DATABASE_URL from environment variable or set a default (PostgreSQL example)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")

