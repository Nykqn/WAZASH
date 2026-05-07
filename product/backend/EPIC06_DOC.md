# EPIC-06 : Docker Compose (Backend) - Documentation

**Date** : 2026-05-07
**Statut** : ✅ Implémenté et testé
**Références** :
- Planification : [`EPIC06_PLAN.md`](./EPIC06_PLAN.md)
- Audit sécurité : [`SECURITY_AUDIT_EPIC06.md`](./SECURITY_AUDIT_EPIC06.md)
- Lab complet : [`EPIC11_DOC.md`](./EPIC11_DOC.md)

## 1. Vue d'ensemble

L'EPIC-06 prépare l'environnement Docker pour le backend WAZASH : Dockerfile optimisé, docker-compose.yml pour l'orchestration, et .dockerignore pour la sécurité.

> **Note** : Le `docker-compose.yml` final se trouve dans `product/docker-compose.yml` et orchestre l'ensemble des services (voir EPIC-11).

## 2. Dockerfile

**Fichier :** `product/backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

# Installer curl pour le healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Virtualenv système
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dépendances (cache optimisé)
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev]"

# Code source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Optimisations

| Optimisation | Description |
|-------------|-------------|
| `python:3.11-slim` | Image légère et officielle |
| `PYTHONDONTWRITEBYTECODE=1` | Évite les fichiers `.pyc` |
| `PIP_NO_CACHE_DIR=1` | Réduit la taille de l'image |
| `pip install -e ".[dev]"` | Installe aussi les dépendances dev (tests) |
| Healthcheck | `curl -f http://localhost:8000/health` |

## 3. .dockerignore

**Fichier :** `product/backend/.dockerignore`

Exclut de l'image Docker :
- `.venv/` et variables d'environnement (`.env`, `.env.*.local`) → **sécurité**
- `__pycache__/`, `*.pyc` → cache inutile
- `.git/` → historique non nécessaire
- `tests/`, `.pytest_cache/` → tests non nécessaires dans l'image runtime
- `*.md` → documentation non nécessaire
- `.vscode/`, `.idea/` → fichiers IDE

## 4. docker-compose.yml (backend uniquement)

**Fichier :** `product/backend/docker-compose.yml` (version simplifiée, le compose final est dans `product/docker-compose.yml`)

**Service wazash-backend :**

| Propriété | Valeur |
|-----------|--------|
| Build | `./backend/Dockerfile` |
| Port | `8000:8000` |
| Dépend | db (service_healthy) |
| Restart | `unless-stopped` |

**Variables d'environnement :**
```yaml
environment:
  - DATABASE_URL=postgresql://wazash:wazash@db:5432/wazash
  - JWT_SECRET_KEY=${JWT_SECRET_KEY:-dev-secret-key-change-in-production}
  - JWT_ALGORITHM=HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 5. Variables d'environnement

### `.env.example` (backend)

```ini
APP_NAME=WAZASH
DEBUG=false
API_V1_PREFIX=/api/v1

# PostgreSQL (production/Docker)
DATABASE_URL=postgresql://wazash:wazash@db:5432/wazash
# SQLite (dev local)
# DATABASE_URL=sqlite:///./wazash.db

JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 6. Commandes Docker

```bash
# Construire et lancer
cd product
docker compose up -d --build

# Vérifier
curl http://localhost:8000/health
# {"status": "ok", "service": "wazash-backend"}

# Logs
docker compose logs -f wazash-backend

# Tests
docker compose exec wazash-backend pytest -v

# Arrêter
docker compose down
```

## 7. Recommandations de production (issues audit)

| Sévérité | Recommandation | Détail |
|----------|---------------|--------|
| ⚠️ Moyen | Utilisateur non-root | Ajouter `USER wazash` dans le Dockerfile |
| ⚠️ Faible | Limites de ressources | Ajouter `deploy.resources.limits` dans docker-compose |
| ⚠️ Faible | Scan d'image | Utiliser `docker scan` ou Trivy avant déploiement |

## 8. Tests

- `docker compose up -d` démarre sans erreur
- `curl http://localhost:8000/health` retourne 200
- `docker compose exec wazash-backend pytest -v` passe (tous les tests)

---

**Validation** : @devops-engineer, @project-manager-tech
