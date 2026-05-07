# Documentation EPIC-02 : Heartbeat & Events Ingestion

**Date d'implémentation** : 2026-05-06  
**Statut** : ✅ Terminé et validé  
**Étape workflow** : 5 - Documentation (après audit sécurité)

## Vue d'ensemble

L'EPIC-02 ajoute la capacité d'ingérer des heartbeats et des événements de sécurité depuis les endpoints WAZASH. Cette fonctionnalité est critique pour le MVP (Priorité 4 et 5).

## Objectifs atteints

- ✅ Endpoint `POST /api/v1/heartbeat` opérationnel
- ✅ Endpoint `POST /api/v1/events` opérationnel
- ✅ Validation stricte des payloads via Pydantic
- ✅ Stockage en mémoire (volatil, pas de persistance)
- ✅ 12 tests pytest passants
- ✅ Aucune dépendance externe ajoutée
- ✅ Aucun secret ou clé API introduit

## Architecture technique

### 1. Schémas Pydantic (Validation)

**`app/heartbeat/schemas.py`**
```python
class HeartbeatPayload(BaseModel):
    endpoint_id: str      # Identifiant unique de l'endpoint
    timestamp: datetime   # Date/heure du heartbeat
    status: str          # État : "up", "down", etc.
```

**`app/events/schemas.py`**
```python
class EventPayload(BaseModel):
    endpoint_id: str      # Identifiant unique de l'endpoint
    timestamp: datetime   # Date/heure de l'événement
    event_type: str       # Type d'événement (ex: "intrusion_detected")
    severity: str         # Sévérité : "high", "medium", "low"
    details: dict         # Détails libres (dict JSON)
```

**Choix technique** : Pydantic assure une validation automatique des types et formats. Si un champ manque ou est du mauvais type, FastAPI retourne automatiquement une erreur 422.

### 2. Stockage en mémoire

**`app/core/storage.py`**

```python
# Stockage en mémoire (listes simples)
heartbeats_store: list[dict[str, Any]] = []
events_store: list[dict[str, Any]] = []

def add_heartbeat(heartbeat: dict[str, Any]) -> None:
    heartbeats_store.append(heartbeat)

def add_event(event: dict[str, Any]) -> None:
    events_store.append(event)

def get_heartbeats() -> list[dict[str, Any]]:
    return heartbeats_store

def get_events() -> list[dict[str, Any]]:
    return events_store
```

**Caractéristiques du stockage :**
- **Volatilité** : Les données sont perdues au redémarrage du serveur
- **Simplicité** : Pas de base de données, pas de Redis, pas de Celery
- **Performance** : Accès direct en mémoire (très rapide)
- **Limites** :
  - Pas de persistance (données perdues à l'arrêt)
  - Pas de lecture d'endpoints GET (non implémenté dans EPIC-02)
  - Stockage limité par la RAM

**Pourquoi ce choix ?**
- Respect strict des contraintes EPIC-02 (pas de DB)
- Adapté pour un MVP et des tests
- Permet de valider le flux d'ingestion avant d'ajouter la persistance

### 3. Routes FastAPI

**`app/heartbeat/router.py`**
```python
@router.post("/heartbeat")
async def receive_heartbeat(payload: HeartbeatPayload) -> dict[str, str]:
    """Reçoit et stocke un heartbeat d'endpoint."""
    add_heartbeat(payload.model_dump())
    return {"status": "ok"}
```

**`app/events/router.py`**
```python
@router.post("/events")
async def receive_event(payload: EventPayload) -> dict[str, str]:
    """Reçoit et stocke un événement de sécurité."""
    add_event(payload.model_dump())
    return {"status": "ok"}
```

Les routes sont incluses dans `app/main.py` avec le préfixe `/api/v1`.

## Tests (12 au total)

### Tests Heartbeat (5 tests)
- `test_heartbeat_valid_payload` : Vérifie l'ingestion avec payload valide (200)
- `test_heartbeat_invalid_payload_missing_field` : Vérifie le rejet si champ manquant (422)
- `test_heartbeat_invalid_payload_wrong_type` : Vérifie le rejet si type incorrect (422)
- `test_heartbeat_storage` : Vérifie que le heartbeat est stocké en mémoire
- `test_heartbeat_multiple_storage` : Vérifie le stockage de plusieurs heartbeats

### Tests Events (5 tests)
- `test_event_valid_payload` : Vérifie l'ingestion avec payload valide (200)
- `test_event_invalid_payload_missing_field` : Vérifie le rejet si champ manquant (422)
- `test_event_invalid_payload_wrong_type` : Vérifie le rejet si type incorrect (422)
- `test_event_storage` : Vérifie que l'événement est stocké en mémoire
- `test_event_multiple_storage` : Vérifie le stockage de plusieurs événements

### Tests Health (2 tests)
- `test_health_check` : Vérifie que `/health` retourne 200
- `test_health_check_no_external_deps` : Vérifie l'absence de dépendances externes

## Exemples d'utilisation

### Heartbeat
```bash
curl -X POST http://localhost:8000/api/v1/heartbeat \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "status": "up"
  }'
```

Réponse : `{"status": "ok"}` (200 OK)

### Événement
```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion_detected",
    "severity": "high",
    "details": {"source_ip": "192.168.1.100", "port": 22}
  }'
```

Réponse : `{"status": "ok"}` (200 OK)

### Payload invalide (exemple)
```bash
curl -X POST http://localhost:8000/api/v1/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"endpoint_id": "ep-001"}'
```

Réponse : 422 Unprocessable Entity avec détails de validation

## Sécurité

L'audit de sécurité (`SECURITY_AUDIT_EPIC02.md`) confirme :
- ✅ Aucun secret codé en dur
- ✅ Aucune clé API (OpenAI ou autre)
- ✅ Validation Pydantic stricte (évite les injections)
- ✅ Stockage mémoire sûr (données volatiles)
- ✅ Aucune commande système dangereuse
- ✅ Aucune dépendance inutile ajoutée

## Limites connues

1. **Pas de persistance** : Les données sont perdues au redémarrage
2. **Pas de endpoints de lecture** : Impossible de récupérer les données stockées via l'API (GET non implémenté)
3. **Stockage limité** : Pas de limite de taille sur les listes en mémoire
4. **Pas de traitement asynchrone** : Ingestion synchrone simple

Ces limites sont **volontaires** pour l'EPIC-02 (MVP). La persistance et la lecture seront ajoutées dans les EPICs futurs.

## Références

- Plan détaillé : `EPIC02_PLAN.md`
- Audit sécurité : `SECURITY_AUDIT_EPIC02.md`
- README principal : `README.md`
- Workflow : `AGENTS.md`

## Prochaines étapes

Selon le workflow WAZASH :
1. ✅ EPIC-02 implémenté
2. ✅ Tests écrits (12 tests)
3. ✅ Audit sécurité validé
4. ✅ Documentation mise à jour (README + EPIC02_DOC.md)
5. ⏭️ Validation par le Chef de Projet (@project-manager-tech)
6. ⏭️ Passage à l'EPIC-03 (Authentification)
