import os
import logging

# ─── Logger Setup ─────────────────────────────────────────────────────────
logger = logging.getLogger("InitEnvironment")
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler("logs/init_environment.log")
f_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(f_handler)

# ─── Mount Directory Structure ────────────────────────────────────────────
MNT_STRUCTURE = {
    "/mnt": [
        "data/raw",
        "data/processed",
        "data/exports",
        "models/llms",
        "models/embeddings",
        "services/shared",
        "tmp",
        "logs",
    ],
    "./logs": [],
    "./runtime": [],
}

def ensure_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Ensured directory: {path}")
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")

def initialize_environment():
    logger.info("[Init] Starting environment setup...")
    for base, subpaths in MNT_STRUCTURE.items():
        if not subpaths:
            ensure_dir(base)
        for sub in subpaths:
            full_path = os.path.join(base, sub)
            ensure_dir(full_path)
    logger.info("[Init] Environment setup complete.")

if __name__ == "__main__":
    initialize_environment()
