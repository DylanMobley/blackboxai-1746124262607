import os
import logging
from pathlib import Path

logger = logging.getLogger("InitEnvironment")
logger.setLevel(logging.INFO)

REQUIRED_DIRS = [
    "logs",
    "mnt/data",
    "mnt/cache",
    "mnt/models",
    "mnt/snapshots",
    "mnt/uploads",
    "mnt/output",
    "mnt/tmp",
    "backend/devtools",
    "backend/tests",
    "microservices",
    "ontology",
    "symbolic",
    "training",
]

REQUIRED_FILES = [
    "logs/.gitkeep",
    "mnt/data/.gitkeep",
    "mnt/cache/.gitkeep"
]

def setup_environment():
    """
    Initializes necessary folders and placeholder files for the project to run in local or production.
    """
    logger.info("[BOOT] Ensuring mount and logs directories exist...")

    for path in REQUIRED_DIRS:
        full_path = Path(path)
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"[✓] Created: {path}")
        else:
            logger.debug(f"[✔] Exists: {path}")

    for file_path in REQUIRED_FILES:
        full_file = Path(file_path)
        if not full_file.exists():
            full_file.touch()
            logger.info(f"[✓] Created: {file_path}")
        else:
            logger.debug(f"[✔] Exists: {file_path}")

    logger.info("[BOOT] Environment structure initialized successfully.")
    return True

if __name__ == "__main__":
    setup_environment()
