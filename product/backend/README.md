# WAZASH Backend

Backend FastAPI pour l'application WAZASH.

## Prérequis

- Python 3.11 ou supérieur
- pip

## Installation et configuration

### 1. Créer l'environnement virtuel

```bash
cd product/backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -e ".[dev]"
```

Ou en une seule commande :

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

### 3. Configuration des variables d'environnement

Copier le fichier d'exemple et l'adapter si nécessaire :

```bash
cp .env.example .env
```

Les variables disponibles sont documentées dans `.env.example`.

## Lancement de l'application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API est accessible sur :
- http://localhost:8000 (API principale)
- http://localhost:8000/docs (Documentation Swagger UI)
- http://localhost:8000/redoc (Documentation ReDoc)

## EPIC-02 Features (Heartbeat & Events Ingestion)

L'EPIC-02 ajoute l'ingestion de heartbeats et d'événements depuis les endpoints WAZASH.

### Endpoints disponibles

#### POST `/api/v1/heartbeat`
Ingestion de heartbeats pour vérifier la disponibilité des endpoints.

**Schéma Pydantic `HeartbeatPayload` :**
```python
class HeartbeatPayload(BaseModel):
    endpoint_id: str      # Identifiant de l'endpoint
    timestamp: datetime   # Date et heure du heartbeat
    status: str          # Statut : "up", "down", etc.
```

**Exemple de payload :**
```json
{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "status": "up"
}
```

#### POST `/api/v1/events`
Ingestion d'événements de sécurité pour détecter des incidents.

**Schéma Pydantic `EventPayload` :**
```python
class EventPayload(BaseModel):
    endpoint_id: str      # Identifiant de l'endpoint
    timestamp: datetime   # Date et heure de l'événement
    event_type: str       # Type d'événement (ex: "intrusion_detected")
    severity: str         # Sévérité : "high", "medium", "low"
    details: dict         # Détails supplémentaires (libre)
```

**Exemple de payload :**
```json
{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion_detected",
    "severity": "high",
    "details": {
        "source_ip": "192.168.1.100",
        "port": 22
    }
}
```

### Stockage en mémoire

Les données sont stockées en mémoire dans des listes Python simples (`heartbeats_store`, `events_store` dans `app/core/storage.py`).

**Caractéristiques :**
- ✅ Stockage volatil (données perdues au redémarrage)
- ✅ Pas de persistance sur disque
- ✅ Pas de base de données, pas de Redis, pas de Celery
- ✅ Adapté pour un MVP et des tests

**Fonctions disponibles dans `app/core/storage.py` :**
- `add_heartbeat(heartbeat)` - Ajoute un heartbeat
- `add_event(event)` - Ajoute un événement
- `get_heartbeats()` - Retourne tous les heartbeats
- `get_events()` - Retourne tous les événements

### Exemples de tests avec curl

**Test heartbeat valide :**
```bash
curl -X POST http://localhost:8000/api/v1/heartbeat \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "status": "up"
  }'
```

**Test événement valide :**
```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion_detected",
    "severity": "high",
    "details": {"source_ip": "192.168.1.100"}
  }'
```

**Test payload invalide (manque un champ) :**
```bash
curl -X POST http://localhost:8000/api/v1/heartbeat \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "status": "up"
  }'
# Retourne 422 Unprocessable Entity
```

## EPIC-03 Features (Authentication)

L'EPIC-03 ajoute un système d'authentification de base (skeleton) pour sécuriser l'API.

> **Références :** Voir [`EPIC03_PLAN.md`](../../EPIC03_PLAN.md) et [`SECURITY_AUDIT_EPIC03.md`](../../SECURITY_AUDIT_EPIC03.md)

### Endpoints disponibles

#### POST `/api/v1/auth/login`
Authentification d'un utilisateur et génération d'un token (fictif pour le MVP).

**Schéma Pydantic `LoginPayload` :**
```python
class LoginPayload(BaseModel):
    email: str      # Adresse email de l'utilisateur
    password: str   # Mot de passe
```

**Exemple de payload :**
```json
{
    "email": "admin@wazash.io",
    "password": "dummy123"
}
```

**Réponse (token fictif) :**
```json
{
    "access_token": "dummy-token-admin",
    "token_type": "bearer"
}
```

### Stockage en mémoire des utilisateurs

Les utilisateurs sont stockés en mémoire dans une liste Python simple (`users_store` dans `app/core/storage.py`).

**Utilisateurs fictifs disponibles :**
- `admin@wazash.io` / `dummy123` (rôle: admin)
- `user@wazash.io` / `dummy123` (rôle: user)

**Caractéristiques :**
- ✅ Stockage volatil (données perdues au redémarrage)
- ✅ Pas de JWT réel (token fictif pour le MVP)
- ✅ Pas de hachage de mot de passe (en clair pour le MVP)
- ✅ Adapté pour un MVP et des tests

### Exemples de tests avec curl

**Login valide (admin) :**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@wazash.io",
    "password": "dummy123"
  }'
```

**Login invalide (mauvais mot de passe) :**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@wazash.io",
    "password": "wrongpassword"
  }'
# Retourne 401 Unauthorized
```

**Login invalide (utilisateur inexistant) :**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@wazash.io",
    "password": "dummy123"
  }'
# Retourne 401 Unauthorized
```

## Tests

Le projet compte **16 tests** répartis comme suit :
- **4 tests auth** (`tests/test_auth.py`) : login valide, login invalide (mauvais mot de passe), login utilisateur inexistant, validation de payload
- **5 tests heartbeat** (`tests/test_heartbeat.py`) : validation de payload, rejet de payload invalide, stockage en mémoire
- **5 tests events** (`tests/test_events.py`) : validation de payload, rejet de payload invalide, stockage en mémoire
- **2 tests health** (`tests/test_health.py`) : vérification du endpoint de santé

Exécuter tous les tests avec pytest :

```bash
pytest -v
```

Exemple de sortie attendue :
```
tests/test_health.py::test_health_check PASSED
tests/test_health.py::test_health_check_no_external_deps PASSED
tests/test_heartbeat.py::test_heartbeat_valid_payload PASSED
tests/test_heartbeat.py::test_heartbeat_invalid_payload_missing_field PASSED
tests/test_heartbeat.py::test_heartbeat_invalid_payload_wrong_type PASSED
tests/test_heartbeat.py::test_heartbeat_storage PASSED
tests/test_heartbeat.py::test_heartbeat_multiple_storage PASSED
tests/test_events.py::test_event_valid_payload PASSED
tests/test_events.py::test_event_invalid_payload_missing_field PASSED
tests/test_events.py::test_event_invalid_payload_wrong_type PASSED
tests/test_events.py::test_event_storage PASSED
tests/test_events.py::test_event_multiple_storage PASSED
tests/test_auth.py::test_login_valid_admin PASSED
tests/test_auth.py::test_login_invalid_password PASSED
tests/test_auth.py::test_login_user_not_found PASSED
tests/test_auth.py::test_login_invalid_payload PASSED

16 passed in X.XXs
```

## Structure du projet

```
product/backend/
├── app/
│   ├── core/
│   │   ├── config.py      # Configuration centralisée
│   │   └── storage.py     # Stockage en mémoire (heartbeats/events/users)
│   ├── auth/
│   │   ├── router.py      # POST /api/v1/auth/login
│   │   └── schemas.py     # Schéma LoginPayload
│   ├── health/
│   │   └── router.py      # Route de health check
│   ├── heartbeat/
│   │   ├── router.py      # POST /api/v1/heartbeat
│   │   └── schemas.py     # Schéma HeartbeatPayload
│   ├── events/
│   │   ├── router.py      # POST /api/v1/events
│   │   └── schemas.py     # Schéma EventPayload
│   └── main.py            # Point d'entrée FastAPI
├── tests/
│   ├── test_health.py     # Tests health (2 tests)
│   ├── test_heartbeat.py  # Tests heartbeat (5 tests)
│   ├── test_events.py     # Tests events (5 tests)
│   └── test_auth.py       # Tests auth (4 tests)
├── pyproject.toml         # Configuration du projet et dépendances
├── .env.example           # Exemple de variables d'environnement
└── README.md              # Ce fichier
```

## Dépannage

### Le port 8000 est déjà utilisé

Modifier le port dans la commande de lancement :

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Problème avec l'environnement virtuel

Supprimer et recréer l'environnement :

```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
