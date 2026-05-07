# ORDER — État du projet WAZASH

*Dernière mise à jour : 2026-05-07 (session 2)*

## Contexte

WAZASH = MVP SOC (FastAPI + SQLAlchemy + PostgreSQL + Frontend vanilla JS).
Stack Docker : backend, frontend (Nginx), PostgreSQL, endpoint-simulator, attacker-simulator.

## Ce qui est fini et commité

### Backend (product/backend/)
- Authentification JWT + RBAC (admin/analyst) — `app/core/security.py`
- Agent auth via `X-API-Key` — `verify_agent_key()` sur POST /heartbeat et /events
- Tous les endpoints protégés : `Depends(get_current_user)` ou `Depends(require_role("admin"))`
- Heartbeat & Events ingestion avec validation Pydantic
- Alertes simples (règles par event_type : intrusion→critique, malware→élevée)
- PATCH /api/v1/alerts/{id} — cycle de vie new/in_review/closed
- Audit trail (login, events, alertes, exports)
- CRUD Assets + auto-enregistrement via heartbeat
- Corrélation IP basique : ≥3 événements même IP en 10min → CorrelationGroup
- CORS configurable via `settings.cors_origins`
- Exports CSV/JSON sur tous les GET endpoints
- Pagination (limit/offset) sur tous les GET endpoints
- GET /auth/me — profil utilisateur courant

### Frontend (product/frontend/)
- GitHub Dark Theme, sidebar, toasts
- Dashboard stats + cards (heartbeats, events, alerts, assets, correlations)
- Sections : Dashboard, Heartbeats, Events, Assets, Alertes, Audit, Corrélations
- Health check dans le footer

### Docker (product/)
- docker-compose.yml — 5 services complètement intégrés
- Simulateurs endpoint-simulator (heartbeat) + attacker-simulator (attaques)

### Tests
- 56/56 pytest pass (sous Docker — PostgreSQL)
- Auth mocks dans `conftest.py` (dependency_overrides)
- Nouveaux tests : PATCH alerte, corrélation IP, /auth/me
- `conftest.py` force `DATABASE_URL` via `os.environ` avant tout import (fix local)

## Mots-clés pour retrouver rapidement

| Mot-clé | Où |
|---------|-----|
| Auth / RBAC | `security.py`, `require_role()`, `get_current_user()` |
| Agent auth | `verify_agent_key()`, `X-API-Key` header |
| Heartbeat | `heartbeat/router.py`, `HeartbeatPayload` schema |
| Events | `events/router.py`, `EventPayload` schema |
| Alertes | `alerts/router.py`, `rules.py`, PATCH statut |
| Audit | `audit/router.py`, `AuditLog` model |
| Assets | `assets/router.py`, auto-register dans heartbeat |
| Corrélation | `correlation/router.py`, `CorrelationGroup` model |
| Dashboard | `frontend/static/app.js`, `loadDashboard()` |
| Frontend nav | `showSection()`, `sectionLoaders` map |
| Docker | `docker-compose.yml`, `Dockerfile` backend/frontend |
| Tests DB | `conftest.py` override `get_db` → SQLite file |
| Conformité | `documents/cahier_des_charges.md` |
| EPIC docs | `product/backend/EPIC*_*.md` |
| Security audits | `product/backend/SECURITY_AUDIT_*.md` |

## État du board GitHub Projects

Board public : https://github.com/Nykqn/WAZASH/projects
Issues #1 à #20 créées, liées au board avec statuts.
- **Done (14)** : #1-#14 (EPICs + features — closed)
- **Done (17)** : #1-#14, #18 (Pagination), #19 (GET /auth/me), #20 (Doc API — closed)
- **In Progress (2)** : #15 Tests corrélation, #17 CORS
- **Todo (1)** : #16 Tests PATCH alerte (reopened, coded but needs Docker rebuild)

## P1 gaps encore ouverts (cahier des charges)

- _(plus aucun — tous les P1 sont implémentés)_

## Problèmes connus

- `git push` bloqué par règle OpenCode — faire manuellement
- Remote URL contient le token (nettoyer après push)
- `.env` contient `JWT_SECRET_KEY=change-me-in-production` — changer pour production
- `datetime.utcnow()` déprécié Python 3.14 — remplacer par `datetime.now(UTC)`

---

**Règle :** Ce fichier DOIT être mis à jour à chaque nouvelle avancée significative (fin de session, nouveau commit, changement de statut de tâche).
