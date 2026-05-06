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

## EPIC-04 Features (Alertes Simples)

L'EPIC-04 ajoute un système d'alertes simples basées sur les événements ingérés (EPIC-02).

> **Références :** Voir [`EPIC04_PLAN.md`](./EPIC04_PLAN.md) et [`SECURITY_AUDIT_EPIC04.md`](./SECURITY_AUDIT_EPIC04.md)

### Règles d'alerte

Le système génère des alertes selon des règles simples :

| Type d'événement | Sévérité de l'alerte |
|------------------|----------------------|
| `intrusion`      | `critical`           |
| `malware`        | `high`               |
| Autres           | Aucune alerte générée |

### Endpoints disponibles

#### GET `/api/v1/alerts/`
Liste toutes les alertes générées, triées par timestamp décroissant.

**Réponse (liste d'alertes) :**
```json
[
  {
    "id": "alert-001",
    "event_id": "event-001",
    "rule_name": "intrusion_detected",
    "severity": "critical",
    "timestamp": "2026-05-06T10:30:00",
    "status": "open"
  }
]
```

#### POST `/api/v1/alerts/generate`
Génération manuelle d'une alerte à partir d'un événement existant.

**Schéma Pydantic `AlertGeneratePayload` :**
```python
class AlertGeneratePayload(BaseModel):
    event_id: str    # Identifiant de l'événement existant
```

**Exemple de payload :**
```json
{
    "event_id": "event-001"
}
```

**Réponse :**
```json
{
    "message": "Alert generated successfully",
    "alert": {
        "id": "alert-001",
        "event_id": "event-001",
        "rule_name": "intrusion_detected",
        "severity": "critical",
        "timestamp": "2026-05-06T10:30:00",
        "status": "open"
    }
}
```

#### Génération automatique après POST `/api/v1/events`
Lors de l'ingestion d'un événement via `POST /api/v1/events`, si le `event_type` correspond à une règle (ex: `intrusion`, `malware`), une alerte est automatiquement générée et stockée.

### Stockage en mémoire

Les alertes sont stockées en mémoire dans une liste Python simple (`alerts_store` dans `app/core/storage.py`).

**Caractéristiques :**
- ✅ Stockage volatil (données perdues au redémarrage)
- ✅ Pas de persistance sur disque
- ✅ Pas de base de données, pas de Redis, pas de Celery
- ✅ Adapté pour un MVP et des tests

**Fonctions disponibles dans `app/core/storage.py` :**
- `add_alert(alert)` - Ajoute une alerte
- `get_alerts()` - Retourne toutes les alertes
- `get_event_by_id(event_id)` - Récupère un événement par son ID

### Exemples de tests avec curl

**POST event intrusion → alerte générée automatiquement :**
```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion",
    "severity": "high",
    "details": {"source_ip": "192.168.1.100"}
  }'
# L'alerte est générée automatiquement
```

**GET alerts pour lister :**
```bash
curl -X GET http://localhost:8000/api/v1/alerts/
# Retourne la liste des alertes
```

**POST alerts/generate avec payload :**
```bash
curl -X POST http://localhost:8000/api/v1/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "event-001"
  }'
# Génère manuellement une alerte pour l'événement event-001
```

## Tests

Le projet compte **24 tests** répartis comme suit :
- **4 tests auth** (`tests/test_auth.py`) : login valide, login invalide (mauvais mot de passe), login utilisateur inexistant, validation de payload
- **5 tests heartbeat** (`tests/test_heartbeat.py`) : validation de payload, rejet de payload invalide, stockage en mémoire
- **5 tests events** (`tests/test_events.py`) : validation de payload, rejet de payload invalide, stockage en mémoire
- **8 tests alerts** (`tests/test_alerts.py`) : génération automatique après event, lecture des alertes, règles d'alerte, génération manuelle, validation de payload
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
tests/test_events.py::test_event_generates_alert_intrusion PASSED
tests/test_events.py::test_event_generates_alert_malware PASSED
tests/test_auth.py::test_login_valid_admin PASSED
tests/test_auth.py::test_login_invalid_password PASSED
tests/test_auth.py::test_login_user_not_found PASSED
tests/test_auth.py::test_login_invalid_payload PASSED
tests/test_alerts.py::test_get_alerts_empty PASSED
tests/test_alerts.py::test_get_alerts_after_event PASSED
tests/test_alerts.py::test_alert_generation_manual PASSED
tests/test_alerts.py::test_alert_generation_event_not_found PASSED
tests/test_alerts.py::test_alert_rule_intrusion_critical PASSED
tests/test_alerts.py::test_alert_rule_malware_high PASSED
tests/test_alerts.py::test_alert_invalid_payload PASSED
tests/test_alerts.py::test_alert_generate_invalid_payload PASSED

24 passed in X.XXs
```

## Structure du projet

```
product/backend/
├── app/
│   ├── core/
│   │   ├── config.py      # Configuration centralisée
│   │   └── storage.py     # Stockage en mémoire (heartbeats/events/users/alerts)
│   ├── auth/
│   │   ├── router.py      # POST /api/v1/auth/login
│   │   └── schemas.py     # Schéma LoginPayload
│   ├── health/
│   │   └── router.py      # Route de health check
│   ├── heartbeat/
│   │   ├── router.py      # POST /api/v1/heartbeat
│   │   └── schemas.py     # Schéma HeartbeatPayload
│   ├── events/
│   │   ├── router.py      # POST /api/v1/events + génération auto alerte
│   │   └── schemas.py     # Schéma EventPayload
│   ├── alerts/
│   │   ├── router.py      # GET /api/v1/alerts + POST /api/v1/alerts/generate
│   │   ├── schemas.py     # Schémas Alert, AlertGeneratePayload
│   │   └── rules.py       # Règles d'alerte (intrusion→critical, malware→high)
│   └── main.py            # Point d'entrée FastAPI
├── tests/
│   ├── test_health.py     # Tests health (2 tests)
│   ├── test_heartbeat.py  # Tests heartbeat (5 tests)
│   ├── test_events.py     # Tests events (5 tests + 2 tests génération alerte auto)
│   ├── test_auth.py       # Tests auth (4 tests)
│   └── test_alerts.py     # Tests alerts (8 tests)
├── pyproject.toml         # Configuration du projet et dépendances
├── .env.example           # Exemple de variables d'environnement
├── EPIC04_PLAN.md          # Planification EPIC-04
├── SECURITY_AUDIT_EPIC04.md # Audit sécurité EPIC-04
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
