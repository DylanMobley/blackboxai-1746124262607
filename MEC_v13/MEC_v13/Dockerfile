# ─── Base ─────────────────────────────────────────────
FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ─── System Setup ─────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# ─── Poetry ───────────────────────────────────────────
ENV POETRY_VERSION=1.7.1

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s ~/.local/bin/poetry /usr/local/bin/poetry

# ─── Working Directory ────────────────────────────────
WORKDIR /app

# ─── Install Dependencies ─────────────────────────────
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# ─── Copy Source ──────────────────────────────────────
COPY . .

# ─── Environment & Volumes ────────────────────────────
ENV ENV_FILE=.env
VOLUME ["/mnt/data", "/mnt/cache", "/mnt/models"]

# ─── Startup ──────────────────────────────────────────
CMD ["poetry", "run", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "5101", "--workers", "4"]
