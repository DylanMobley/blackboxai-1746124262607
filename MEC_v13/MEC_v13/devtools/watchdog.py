import os
import subprocess
import time
from config.logging_config import setup_logger

logger = setup_logger("Watchdog", "logs/watchdog.log")

# Paths to monitor (can be extended)
TARGET_SCRIPTS = {
    "API": "backend/api.py",
    "CLONE": "microservices/emotion-clone-stack/clone_service.py"
}

def launch_process(name, path):
    logger.info(f"🚀 Starting {name} → {path}")
    return subprocess.Popen(["python", path])

def monitor():
    processes = {}
    for name, path in TARGET_SCRIPTS.items():
        processes[name] = launch_process(name, path)

    while True:
        for name, proc in processes.items():
            if proc.poll() is not None:
                logger.warning(f"⚠️ {name} crashed. Restarting...")
                processes[name] = launch_process(name, TARGET_SCRIPTS[name])
        time.sleep(5)

if __name__ == "__main__":
    logger.info("🛡️ Watchdog online...")
    monitor()
