# EPIC-09 : GET endpoints + exports CSV + frontend SOC - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Lecture des données, exports, dashboard SOC

## 1. Objectif
Ajouter des endpoints GET pour lire les données stockées (heartbeats, events, alerts, audit, assets) avec filtres optionnels et export au format CSV. Déployer un frontend SOC dashboard (HTML/CSS/JS) pour visualiser ces données.

## 2. User Stories
- **US-09.1** : En tant que SOC, je consulte la liste des heartbeats avec filtres et export CSV.
- **US-09.2** : En tant que SOC, je consulte la liste des événements avec filtres et export CSV.
- **US-09.3** : En tant que SOC, je consulte les alertes avec filtres et export CSV.
- **US-09.4** : En tant que SOC, je consulte les logs d'audit avec filtres et export CSV.
- **US-09.5** : En tant que SOC, j'accède à un dashboard web pour visualiser l'état du système.

## 3. Fichiers à créer/modifier
- `app/heartbeat/router.py` : Ajout GET `/heartbeats` avec filtres (endpoint_id, status, format)
- `app/events/router.py` : Ajout GET `/events` avec filtres (endpoint_id, event_type, severity, format)
- `app/alerts/router.py` : Ajout filtres (severity, status, format) sur GET `/alerts/`
- `app/audit/router.py` : Ajout filtres (action, user_email, format) sur GET `/audit/`
- `app/assets/router.py` : Ajout filtre status_filter + format CSV sur GET `/assets/`
- `product/frontend/index.html` : Dashboard SOC complet
- `product/frontend/static/app.js` : Logique frontend (login, API calls, table rendering)
- `product/frontend/static/style.css` : Thème sombre SOC
- `product/frontend/Dockerfile` : Image Nginx pour le frontend
- `product/frontend/nginx.conf` : Reverse proxy vers le backend
- `tests/test_exports.py` : Tests exports CSV et filtres

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- GET `/api/v1/heartbeats` retourne la liste avec filtres (status, endpoint_id, format=csv)
- GET `/api/v1/events` retourne la liste avec filtres (event_type, severity, endpoint_id, format=csv)
- GET `/api/v1/alerts/` retourne la liste avec filtres (severity, status, format=csv)
- GET `/api/v1/audit/` retourne la liste avec filtres (action, user_email, format=csv)
- GET `/api/v1/assets/` retourne la liste avec filtre status + format=csv
- Frontend accessible sur port 8080, proxy vers backend sur /api/
- Authentification JWT gérée côté frontend (login → token → dashboard)
- Tous les tests pytest passent

## 6. Tests attendus (11 dans test_exports.py)
- `test_get_heartbeats_json` : GET heartbeats format JSON
- `test_get_heartbeats_csv` : GET heartbeats format CSV
- `test_get_heartbeats_filter_status` : Filtre par status
- `test_get_events_json` : GET events format JSON
- `test_get_events_csv` : GET events format CSV
- `test_get_events_filter_severity` : Filtre par severity
- `test_get_alerts_csv` : GET alerts format CSV
- `test_get_alerts_filter_status` : Filtre par status
- `test_get_audit_csv` : GET audit format CSV
- `test_get_audit_filter_action` : Filtre par action

## 7. Risques
- CORS mal configuré bloquant les requêtes frontend
- Exposition de données sensibles via les GET endpoints non authentifiés
- Frontend sans protection CSRF
- URL backend en dur dans le frontend (192.168.1.31:8000)
- Performances des exports CSV avec gros volumes

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @backend-python-dev)
