# ORDER — État du projet WAZASH

*Dernière mise à jour : 2026-05-07*

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

### Frontend (product/frontend/)
- GitHub Dark Theme, sidebar, toasts
- Dashboard stats + cards (heartbeats, events, alerts, assets, correlations)
- Sections : Dashboard, Heartbeats, Events, Assets, Alertes, Audit, Corrélations
- Health check dans le footer

### Docker (product/)
- docker-compose.yml — 5 services complètement intégrés
- Simulateurs endpoint-simulator (heartbeat) + attacker-simulator (attaques)

### Tests
- 50/50 pytest pass (sous Docker — PostgreSQL)
- Auth mocks dans `conftest.py` (dependency_overrides)

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
- **In Progress (3)** : #15 Tests corrélation, #16 Tests PATCH, #17 CORS
- **Todo (3)** : #18 Pagination, #19 GET /auth/me, #20 Documentation API

## P1 gaps encore ouverts (cahier des charges)

- Pagination GET endpoints
- Endpoint GET /auth/me (profil courant)
- Tests dédiés pour corrélation et PATCH alerte

## Problèmes connus

- `.env` pointe vers PostgreSQL — les tests hors Docker échouent
- `git push` bloqué par règle OpenCode — faire manuellement
- Remote URL contient le token (nettoyer après push)
- `.env` contient `JWT_SECRET_KEY=change-me-in-production` — changer pour production
- Token GitHub scope `project` nécessaire pour modifier le board

---

**Règle :** Ce fichier DOIT être mis à jour à chaque nouvelle avancée significative (fin de session, nouveau commit, changement de statut de tâche).
