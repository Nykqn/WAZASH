# WAZASH

> **Wa**zash **A**nalyzer for **S**OC & **H**unting — Plateforme de cybersurveillance réseau orientée SOC.

WAZASH est un laboratoire SOC (Security Operations Center) clé en main qui simule une infrastructure de détection d'intrusions complète : collecte de télémétrie, ingestion d'événements, détection par règles, alertes actionnables, inventaire d'actifs, audit trail, et dashboard de visualisation.

---

## Fonctionnalités

| Module | Description |
|--------|-------------|
| **Heartbeat** | Réception de signaux de vie depuis les endpoints surveillés |
| **Events** | Ingestion d'événements de sécurité (intrusion, malware, scan) |
| **Assets** | Inventaire d'actifs avec auto-enregistrement automatique |
| **Alertes** | Détection par règles simples (intrusion → critique, malware → élevée) |
| **Audit Trail** | Journalisation de toutes les actions système |
| **Exports CSV** | Export de toutes les données au format CSV |
| **Dashboard SOC** | Interface web temps réel (thème sombre GitHub-style) |
| **Simulateurs** | Endpoint Simulator (heartbeats) + Attacker Simulator (attaques) |

## Architecture

```
                    ┌──────────────────┐
                    │   Frontend       │  Port 8080
                    │   Nginx + HTML   │
                    └────────┬─────────┘
                             │ proxy /api/
                    ┌────────▼─────────┐
                    │   Backend        │  Port 8000
                    │   FastAPI        │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌───────▼──────┐  ┌───▼────────┐
     │ PostgreSQL  │  │Endpoint Sim  │  │Attacker Sim│
     │   Port 5432 │  │ heartbeats   │  │  attaques  │
     └─────────────┘  └──────────────┘  └────────────┘
```

## Démarrage rapide (Docker)

### Prérequis

- Docker
- Docker Compose (intégré à Docker)

### Lancer le lab complet

```bash
git clone <votre-repo> wazash
cd wazash/product

# Copier les variables d'environnement
cp backend/.env.example backend/.env

# Lancer tous les services
docker compose up -d --build
```

### Vérifier l'installation

```bash
# API Health
curl http://localhost:8000/health
# → {"status":"ok","service":"wazash-backend"}

# Dashboard SOC
# Ouvrir http://localhost:8080 dans un navigateur
# Identifiants : admin@wazash.io / dummy123
```

### Services

| Service | URL | Description |
|---------|-----|-------------|
| Dashboard SOC | `http://localhost:8080` | Interface d'administration |
| API Backend | `http://localhost:8000` | API REST FastAPI |
| Documentation API | `http://localhost:8000/docs` | Swagger UI |
| PostgreSQL | `localhost:5432` | Base de données |

## API REST

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/auth/login` | Authentification |
| `POST` | `/api/v1/heartbeat` | Envoyer un heartbeat |
| `GET` | `/api/v1/heartbeats` | Lister les heartbeats (filtres: `?status=`, `?endpoint_id=`, `?format=csv`) |
| `POST` | `/api/v1/events` | Envoyer un événement |
| `GET` | `/api/v1/events` | Lister les événements (filtres: `?severity=`, `?event_type=`, `?format=csv`) |
| `GET` | `/api/v1/alerts/` | Lister les alertes (filtres: `?severity=`, `?status=`, `?format=csv`) |
| `POST` | `/api/v1/alerts/generate` | Générer une alerte manuellement |
| `GET` | `/api/v1/audit/` | Lister les logs d'audit (filtres: `?action=`, `?user_email=`, `?format=csv`) |
| `GET` | `/api/v1/assets/` | Lister les actifs (filtre: `?status_filter=`, `?format=csv`) |
| `POST` | `/api/v1/assets/` | Ajouter un actif |
| `PATCH` | `/api/v1/assets/{endpoint_id}` | Modifier un actif |
| `DELETE` | `/api/v1/assets/{endpoint_id}` | Supprimer un actif |

### Authentification

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@wazash.io", "password": "dummy123"}'

# Utiliser le token
curl http://localhost:8000/api/v1/events \
  -H "Authorization: Bearer <token>"
```

## Comptes par défaut

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| `admin@wazash.io` | `dummy123` | Administrateur |
| `user@wazash.io` | `test456` | Analyste |

## Simulation d'attaques

Le lab inclut deux simulateurs qui s'exécutent automatiquement dans Docker :

- **Endpoint Simulator** : Envoie des heartbeats toutes les 10s pour 4 endpoints (95% up, 5% down)
- **Attacker Simulator** : Envoie des attaques aléatoires toutes les ~30s (intrusion SSH, SQL injection, malware, scan)

## Structure du projet

```
WAZASH/
├── product/
│   ├── backend/          # API FastAPI + SQLAlchemy
│   │   ├── app/          # Code source
│   │   │   ├── auth/     # Authentification JWT
│   │   │   ├── alerts/   # Règles et alertes
│   │   │   ├── assets/   # Inventaire d'actifs
│   │   │   ├── audit/    # Audit trail
│   │   │   ├── events/   # Gestion des événements
│   │   │   ├── health/   # Health check
│   │   │   ├── heartbeat/# Heartbeat ingestion
│   │   │   ├── models/   # Modèles SQLAlchemy
│   │   │   └── core/     # Configuration, sécurité, stockage
│   │   ├── tests/        # Tests pytest
│   │   └── *.md          # Plans, documentation, audits
│   ├── frontend/         # Dashboard SOC (HTML/CSS/JS + Nginx)
│   ├── docker-compose.yml
│   ├── endpoint-simulator/
│   └── attacker-simulator/
├── .opencode/            # Workflow et agents OpenCode
├── architecture.md
└── AGENTS.md
```

## Développement local (sans Docker)

```bash
cd product/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
# Dans le conteneur Docker
docker compose exec wazash-backend pytest -v

# En local
cd product/backend && source .venv/bin/activate && pytest -v
```

## Workflow de développement

Ce projet suit un workflow agentic OpenCode :

1. **project-manager-tech** : Planifie et valide
2. **backend-python-dev** : Implémente le backend
3. **qa-tester** : Écrit les tests
4. **security-tech-lead** : Audite la sécurité
5. **devops-engineer** : Prépare Docker et CI/CD

Voir [`AGENTS.md`](./AGENTS.md) pour les détails.

---

**Version** : 0.3 — Lab SOC WAZASH
