# EPIC-02 : Heartbeat & Events Ingestion - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par le Chef de Projet)
**Lien MVP** : Priorité 4 (heartbeat) et 5 (events)

## 1. Objectif
Implémenter l'ingestion de heartbeat et d'événements depuis les endpoints WAZASH, avec stockage en mémoire (pas de base de données), validation des payloads, et tests associés.

## 2. User Stories
- **US-02-01** : En tant que SOC, je reçois des heartbeats depuis les endpoints pour vérifier leur disponibilité.
- **US-02-02** : En tant que SOC, j'ingère des événements de sécurité depuis les endpoints pour détecter des incidents.

## 3. Fichiers à créer/modifier
- `product/backend/app/heartbeat/router.py` (POST `/api/v1/heartbeat`)
- `product/backend/app/heartbeat/schemas.py` (Schéma Pydantic heartbeat)
- `product/backend/app/events/router.py` (POST `/api/v1/events`)
- `product/backend/app/events/schemas.py` (Schéma Pydantic events)
- `product/backend/app/core/storage.py` (Stockage en mémoire temporaire)
- `product/backend/app/main.py` (Inclusion des nouveaux routers)
- `product/backend/tests/test_heartbeat.py` (Tests pytest heartbeat)
- `product/backend/tests/test_events.py` (Tests pytest events)

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- POST `/api/v1/heartbeat` et `/api/v1/events` retournent 200 pour payloads valides
- Payloads invalides retournent 422 (validation Pydantic)
- Stockage en mémoire (pas de persistance, pas de DB/Redis/Celery)
- Aucun appel OpenAI, aucun secret réel, aucun frontend
- Tous les tests pytest passent

## 6. Tests attendus
- Validation de schéma pour heartbeat/events
- Test de réception de payload valide (200)
- Test de rejet de payload invalide (422)
- Test de stockage en mémoire (vérification d'ajout)

## 7. Risques
- Sur-ingénierie du stockage (rester en mémoire)
- Oubli de validation des payloads
- Inclusion de dépendances interdites (DB, Redis, Celery, OpenAI)

## 8. Validation
✅ Plan validé par le Chef de Projet
✅ Prêt pour l'étape 2 (Développement)
