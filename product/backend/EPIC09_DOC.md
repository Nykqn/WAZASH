# EPIC-09 : GET endpoints + exports CSV + frontend SOC - Documentation

**Date** : 2026-05-06
**Statut** : ✅ Implémenté et testé
**Références** :
- Planification : [`EPIC09_PLAN.md`](./EPIC09_PLAN.md)
- Audit sécurité : [`SECURITY_AUDIT_EPIC09.md`](./SECURITY_AUDIT_EPIC09.md)

## 1. Vue d'ensemble

L'EPIC-09 ajoute des endpoints de lecture (GET) pour toutes les données WAZASH avec filtres paramétrables et export au format CSV. Un dashboard frontend complet (HTML/CSS/JS) permet aux opérateurs SOC de visualiser l'état du système.

## 2. GET endpoints et filtres

### 2.1 GET `/api/v1/heartbeats`

Liste des heartbeats avec filtres optionnels.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `endpoint_id` | string | Filtre par endpoint |
| `status` | string | Filtre par statut (`up`, `down`) |
| `format` | string | `json` (défaut) ou `csv` |

### 2.2 GET `/api/v1/events`

Liste des événements avec filtres optionnels.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `endpoint_id` | string | Filtre par endpoint |
| `event_type` | string | Filtre par type d'événement |
| `severity` | string | Filtre par sévérité (`high`, `medium`, `low`) |
| `format` | string | `json` (défaut) ou `csv` |

### 2.3 GET `/api/v1/alerts/`

Liste des alertes avec filtres optionnels.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `severity` | string | Filtre par sévérité (`critical`, `high`) |
| `status` | string | Filtre par statut (`open`, `closed`) |
| `format` | string | `json` (défaut) ou `csv` |

### 2.4 GET `/api/v1/audit/`

Liste des logs d'audit avec filtres optionnels.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `action` | string | Filtre par action (`login`, `event_ingested`, `alert_generated`, etc.) |
| `user_email` | string | Filtre par email utilisateur |
| `format` | string | `json` (défaut) ou `csv` |

### 2.5 GET `/api/v1/assets/`

Liste des actifs avec filtre optionnel.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `status_filter` | string | Filtre par statut (`active`, `inactive`, `down`) |
| `format` | string | `json` (défaut) ou `csv` |

## 3. Export CSV

Tous les GET endpoints supportent le paramètre `?format=csv` qui retourne les données au format CSV avec en-têtes. Le Content-Type est `text/csv`.

**Exemple :**
```bash
curl -X GET "http://localhost:8000/api/v1/events?format=csv"
# id,endpoint_id,timestamp,event_type,severity,details,created_at
# 1,ep-001,2026-05-06T10:30:00,intrusion,high,"{""source_ip"": ""192.168.1.100""}",2026-05-06T10:30:00
```

## 4. Frontend SOC Dashboard

### 4.1 Architecture

```
product/frontend/
├── Dockerfile        # Image Nginx Alpine
├── index.html        # Page principale (login + dashboard)
├── nginx.conf        # Reverse proxy vers le backend
└── static/
    ├── app.js        # Logique frontend (auth, API, UI)
    └── style.css     # Thème sombre SOC
```

### 4.2 Fonctionnalités

| Section | Fonctionnalité |
|---------|---------------|
| **Login** | Authentification JWT, session storage, expiration check |
| **Health** | Vérification de l'état du backend |
| **Heartbeats** | Envoi, liste avec statuts (up/down), export CSV |
| **Events** | Envoi, liste avec sévérités (high/medium/low), export CSV |
| **Assets** | Création, liste avec hostname/IP/OS, suppression, export CSV, auto-registration |
| **Alerts** | Liste avec sévérités (critical/high), export CSV |
| **Audit** | Liste des logs d'audit avec user et détails, export CSV |

### 4.3 Authentification

Le frontend gère l'authentification via JWT :
- Login → stockage du token dans `localStorage`
- Envoi du token dans le header `Authorization: Bearer <token>`
- Vérification d'expiration automatique (`isTokenExpired()`)
- Redirection vers login si 401

### 4.4 Configuration réseau

- Le frontend est servi sur le port 8080
- Nginx proxy les requêtes `/api/` vers `http://wazash-backend:8000/api/`
- Le frontend utilise directement l'IP `192.168.1.31:8000` pour les appels API (configuration réseau locale)

## 5. Tests

L'EPIC-09 ajoute **11 tests** dans `tests/test_exports.py` :

| Test | Description |
|------|-------------|
| `test_get_heartbeats_json` | GET /heartbeats retourne JSON |
| `test_get_heartbeats_csv` | GET /heartbeats?format=csv retourne CSV |
| `test_get_heartbeats_filter_status` | Filtre par status='down' |
| `test_get_events_json` | GET /events retourne JSON |
| `test_get_events_csv` | GET /events?format=csv retourne CSV |
| `test_get_events_filter_severity` | Filtre par severity='high' |
| `test_get_alerts_csv` | GET /alerts/?format=csv retourne CSV |
| `test_get_alerts_filter_status` | Filtre par status='open' |
| `test_get_audit_csv` | GET /audit/?format=csv retourne CSV |
| `test_get_audit_filter_action` | Filtre par action='login' |

## 6. Limites et contraintes

### 6.1 Limites actuelles
1. **Pas de pagination** sur les GET endpoints
2. **URL backend en dur** dans le code frontend (`192.168.1.31:8000`)
3. **Pas de tri personnalisé** (ordre décroissant par timestamp uniquement)
4. **Pas de mise à jour en temps réel** (rafraîchissement manuel)

### 6.2 Contraintes respectées
- ✅ Exports CSV disponibles sur tous les endpoints
- ✅ Filtres paramétrables
- ✅ Frontend responsive (thème sombre)
- ✅ Gestion des erreurs (401 → déconnexion)
- ✅ Aucune dépendance frontend (vanilla JS, pas de framework)

---

**Validation** : @project-manager-tech, @security-tech-lead
