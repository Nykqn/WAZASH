# =============================================================================
# WAZASH Backend - Dockerfile (EPIC-07)
# Image basée sur python:3.11-slim pour une empreinte minimale
# =============================================================================

FROM python:3.11-slim

# Installer curl pour le healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Création du répertoire de travail
WORKDIR /app

# Création du virtualenv système
RUN python -m venv /opt/venv

# Ajout du venv au PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copie des fichiers de dépendances en premier (optimisation du cache Docker)
COPY pyproject.toml .

# Installation des dépendances (y compris les dépendances dev pour les tests)
RUN pip install --no-cache-dir -e ".[dev]"

# Copie du reste du code source
COPY . .

# Exposition du port 8000
EXPOSE 8000

# Commande de lancement de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
