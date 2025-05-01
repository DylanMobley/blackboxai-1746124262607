# microservices/emotion-tts/Dockerfile

# ─── Base Image ─────────────────────────────────────
FROM python:3.10-slim

# ─── Set Working Directory ───────────────────────────
WORKDIR /app

# ─── Install System Dependencies ─────────────────────
RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ─── Copy Service Files ─────────────────────────────
COPY . /app/

# ─── Install Python Packages ────────────────────────
RUN pip install --no-cache-dir flask flask-cors soundfile numpy simpleaudio \
    && pip install bark  # or appropriate Bark variant if locally modded

# ─── Ports ──────────────────────────────────────────
EXPOSE 5111

# ─── Command ─────────────────────────────────────────
CMD ["python", "emotion_tts_service.py"]
