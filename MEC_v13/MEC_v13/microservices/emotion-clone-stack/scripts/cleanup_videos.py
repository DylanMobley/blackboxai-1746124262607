import os
import time
from config.logging_config import setup_logger
from config.security_policy import (
    VIDEO_RETENTION_HOURS,
    AUDIO_RETENTION_HOURS
)

logger = setup_logger("Cleanup", "logs/cleanup.log")

# Paths (can be refactored to .env or centralized config)
VIDEO_FOLDER = "video"
AUDIO_FOLDER = "audio"

def clean_folder(path: str, extensions: list, retention_hours: int):
    """
    Remove files older than retention policy.
    """
    cutoff = time.time() - (retention_hours * 3600)
    if not os.path.exists(path):
        logger.warning(f"❌ Folder missing: {path}")
        return

    deleted = 0
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if not os.path.isfile(file_path):
            continue
        if not any(filename.endswith(ext) for ext in extensions):
            continue

        file_time = os.path.getmtime(file_path)
        if file_time < cutoff:
            try:
                os.remove(file_path)
                deleted += 1
                logger.info(f"🗑 Deleted: {filename}")
            except Exception as e:
                logger.error(f"⚠️ Failed to delete {filename}: {e}", exc_info=True)

    logger.info(f"✅ {deleted} files cleaned in {path}")

def run_cleanup():
    logger.info("🧼 Running media cleanup...")
    clean_folder(VIDEO_FOLDER, [".mp4"], VIDEO_RETENTION_HOURS)
    clean_folder(AUDIO_FOLDER, [".wav"], AUDIO_RETENTION_HOURS)
    logger.info("✅ Cleanup complete.")

if __name__ == "__main__":
    run_cleanup()
