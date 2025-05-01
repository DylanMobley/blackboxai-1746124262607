#!/bin/bash
# ───────────────────────────────────────────────
# CRON WRAPPER: Runs cleanup_videos.py in logs
# Add to crontab: 0 * * * * /path/to/cron_cleanup.sh
# ───────────────────────────────────────────────

echo "[🧼 CLEANUP] Starting: $(date)" >> /var/log/mec_cleanup.log

cd /app/microservices/emotion-clone-stack/
python3 cleanup_videos.py >> /var/log/mec_cleanup.log 2>&1

echo "[✅ DONE] $(date)" >> /var/log/mec_cleanup.log
