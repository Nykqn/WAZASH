# EPIC-11 : Lab Docker Complet (frontend + endpoint + attacker)

**Date** : 2026-05-07
**Statut** : ✅ Implémenté et déployé
**Référence** : [`docker-compose.yml`](../docker-compose.yml)

## 1. Vue d'ensemble

Le lab Docker WAZASH orchestre 5 services interconnectés pour simuler un environnement SOC complet. Le déploiement se fait avec une seule commande `docker compose up`.

## 2. Architecture du lab

```
┌─────────────────────────────────────────────────────────┐
│                    wazash-net (bridge)                    │
│                                                          │
│  ┌──────────────┐     ┌──────────────────┐              │
│  │  Frontend     │────▶│   Backend         │              │
│  │  Nginx:8080   │     │   FastAPI:8000    │              │
│  └──────────────┘     └────────┬─────────┘              │
│                                │                          │
│                    ┌───────────┴───────────┐              │
│                    │                       │              │
│          ┌─────────▼──────┐     ┌──────────▼─────────┐   │
│          │  PostgreSQL    │     │   Redis (Celery)    │   │
│          │  :5432         │     │   (réservé)         │   │
│          └────────────────┘     └────────────────────┘   │
│                    │                       │              │
│          ┌─────────▼──────┐     ┌──────────▼─────────┐   │
│          │  Endpoint Sim  │     │  Attacker Sim       │   │
│          │  (heartbeats)  │     │  (attaques)          │   │
│          └────────────────┘     └────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 3. Services

### 3.1 wazash-backend

| Propriété | Valeur |
|-----------|--------|
| **Image** | Build local (`./backend/Dockerfile`) |
| **Base** | `python:3.11-slim` |
| **Port** | `8000:8000` |
| **Dépend** | db (service_healthy) |

**Variables d'environnement :**
- `PYTHONUNBUFFERED=1`
- `DATABASE_URL=postgresql://wazash:wazash@db:5432/wazash`
- `JWT_SECRET_KEY=${JWT_SECRET_KEY}`
- `JWT_ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`

**Healthcheck :** `curl -f http://localhost:8000/health` (toutes les 30s, start_period 40s)

### 3.2 wazash-frontend

| Propriété | Valeur |
|-----------|--------|
| **Image** | Build local (`./frontend/Dockerfile`) |
| **Base** | `nginx:alpine` |
| **Port** | `8080:80` |
| **Dépend** | wazash-backend |

**Configuration :** Nginx sert les fichiers statiques et proxy les requêtes `/api/` et `/health` vers le backend.

### 3.3 db

| Propriété | Valeur |
|-----------|--------|
| **Image** | `postgres:16-alpine` |
| **Port** | `5432:5432` |
| **Volume** | `postgres_data:/var/lib/postgresql/data` |

**Identifiants :** `wazash` / `wazash` / `wazash`

**Healthcheck :** `pg_isready -U wazash -d wazash` (toutes les 10s)

### 3.4 endpoint-simulator

| Propriété | Valeur |
|-----------|--------|
| **Image** | Build local (`./endpoint-simulator/Dockerfile`) |
| **Base** | `python:3.11-slim` |
| **Dépend** | wazash-backend |

**Comportement :** Envoie des heartbeats toutes les 10s pour les endpoints configurés :
- `ep-web-01`, `ep-db-01`, `ep-fw-01`, `ep-wks-01`
- 95% de chance d'être "up", 5% "down"

**Variables d'environnement :**
- `API_BASE=http://wazash-backend:8000/api/v1`
- `ENDPOINTS=ep-web-01,ep-db-01,ep-fw-01,ep-wks-01`
- `INTERVAL_SECONDS=10`

### 3.5 attacker-simulator

| Propriété | Valeur |
|-----------|--------|
| **Image** | Build local (`./attacker-simulator/Dockerfile`) |
| **Base** | `python:3.11-slim` |
| **Dépend** | wazash-backend |

**Comportement :** Envoie des événements d'attaque aléatoires toutes les ~30s :
- **intrusion** (ssh_bruteforce, sql_injection)
- **malware** (Trojan.Gen)
- **scan** (nmap)

**Variables d'environnement :**
- `API_BASE=http://wazash-backend:8000/api/v1`
- `INTERVAL_SECONDS=30`

## 4. Réseau et volumes

- **Réseau** : `wazash-net` (bridge) — tous les services communiquent via ce réseau
- **Volume** : `postgres_data` — persistance des données PostgreSQL

## 5. Commandes

### Démarrage
```bash
cd product
docker compose up -d --build
```

### Vérification
```bash
# Health check
curl http://localhost:8000/health

# Frontend
curl http://localhost:8080

# Logs backend
docker compose logs -f wazash-backend

# Tests dans le conteneur
docker compose exec wazash-backend pytest -v
```

### Arrêt
```bash
docker compose down        # Arrêt
docker compose down -v     # Arrêt + suppression volumes
```

## 6. Dépendances entre services

```
db ──> wazash-backend ──> wazash-frontend
                        ──> endpoint-simulator
                        ──> attacker-simulator
```

- `wazash-backend` attend que `db` soit healthy
- `wazash-frontend`, `endpoint-simulator` et `attacker-simulator` dépendent de `wazash-backend`

## 7. Recommandations (issues EPIC-06)

### 7.1 Ajouter un utilisateur non-root
```dockerfile
RUN useradd -m -u 1000 wazash && chown -R wazash:wazash /app
USER wazash
```

### 7.2 Ajouter des limites de ressources
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

## 8. Limites actuelles
- Les tests (`tests/`) sont exclus de l'image Docker (`.dockerignore`)
- Pas de limite de ressources CPU/mémoire
- Exécution en root dans le conteneur
- Pas de réseau externe configuré (accessible en local uniquement)
- Pas de service Redis/Celery actif (réservé pour futur)

---

**Validation** : @devops-engineer, @project-manager-tech
