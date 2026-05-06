# EPIC-05 : Audit Trail - Documentation

## Vue d'ensemble

L'EPIC-05 ajoute un système d'audit trail automatique pour tracer les actions importantes du système WAZASH. Ce système permet de suivre qui fait quoi et quand, ce qui est essentiel pour un SOC (Security Operations Center).

## Fonctionnalités implémentées

### 1. Système d'audit trail automatique
- Stockage en mémoire des logs d'audit dans `app/core/storage.py` (`audit_logs_store`)
- Génération automatique de logs lors d'actions critiques
- Format de log structuré : `id`, `timestamp`, `action`, `user_email`, `details`

### 2. Actions tracées
| Action | Déclencheur | user_email |
|--------|-------------|------------|
| `login` | Succès de `POST /api/v1/auth/login` | Email de l'utilisateur |
| `event_ingested` | Succès de `POST /api/v1/events` | `null` (système) |
| `alert_generated` | Génération d'alerte (auto ou manuelle) | `null` (système) |

### 3. Endpoint d'audit
- **GET `/api/v1/audit/`** : Liste tous les logs d'audit par ordre chronologique inversé
- Pas d'authentification requise pour ce MVP (voir Limites)

## Intégration dans les modules existants

### Auth (`app/auth/router.py`)
Après un login réussi, un log d'audit est automatiquement créé :
```python
# Après validation du login
add_audit_log(
    action="login",
    user_email=user["email"],
    details={"email": user["email"]}
)
```

### Events (`app/events/router.py`)
Après ingestion d'un événement, un log d'audit est créé :
```python
# Après ajout de l'événement
add_audit_log(
    action="event_ingested",
    user_email=None,
    details={
        "event_id": event["id"],
        "event_type": event["event_type"],
        "endpoint_id": event["endpoint_id"]
    }
)
```

### Alerts (`app/alerts/router.py`)
Après génération d'une alerte (automatique ou manuelle) :
```python
# Après création de l'alerte
add_audit_log(
    action="alert_generated",
    user_email=None,
    details={
        "alert_id": alert["id"],
        "event_id": alert["event_id"],
        "rule_name": alert["rule_name"]
    }
)
```

## Stockage en mémoire

Les logs d'audit utilisent le même mécanisme de stockage que les autres modules (heartbeats, events, alerts, users) :
- Liste Python simple : `audit_logs_store = []`
- Fonction d'ajout : `add_audit_log(action, user_email, details)`
- Fonction de lecture : `get_audit_logs()` (retourne les logs du plus récent au plus ancien)

**Caractéristiques :**
- ✅ Stockage volatil (données perdues au redémarrage)
- ✅ Pas de persistance sur disque
- ✅ Pas de base de données, pas de Redis
- ✅ Adapté pour un MVP et des tests

## Format des logs d'audit

```json
{
  "id": "audit-001",
  "timestamp": "2026-05-06T10:30:00",
  "action": "login",
  "user_email": "admin@wazash.io",
  "details": {
    "email": "admin@wazash.io"
  }
}
```

**Champs :**
- `id` : Identifiant unique du log (format "audit-XXX")
- `timestamp` : Date et heure de l'action (ISO 8601)
- `action` : Type d'action (`login`, `event_ingested`, `alert_generated`)
- `user_email` : Email de l'utilisateur (si applicable, sinon `null`)
- `details` : Dictionnaire contenant les détails spécifiques à l'action

## Tests

L'EPIC-05 ajoute **5 tests** dans `tests/test_audit.py` :
1. **test_get_audit_logs_empty** : Vérifie que la liste est vide au démarrage
2. **test_audit_log_format** : Vérifie le format des logs (champs requis)
3. **test_audit_log_after_login** : Vérifie qu'un log est créé après un login
4. **test_audit_log_after_event** : Vérifie qu'un log est créé après un événement
5. **test_audit_log_after_alert** : Vérifie qu'un log est créé après une alerte

Ces tests portent le total à **29 tests** pour le backend.

## Limites et considérations

### ⚠️ Pas d'authentification sur `/api/v1/audit/`
Pour le MVP, l'endpoint d'audit est accessible sans authentification. Cela présente des risques :
- N'importe qui peut lire les logs d'audit
- Pas de filtrage par utilisateur ou par action

**Recommandation pour la production :**
- Ajouter une dépendance d'authentification sur l'endpoint `/api/v1/audit/`
- Implémenter un système de rôles (seuls les admins peuvent voir les logs)
- Ajouter des filtres (par date, par action, par utilisateur)

### Autres limites du MVP
- Stockage en mémoire uniquement (perte des logs au redémarrage)
- Pas de pagination sur `GET /api/v1/audit/` (tous les logs sont retournés)
- Pas de nettoyage automatique des anciens logs
- Format des logs fixe (pas d'extension possible sans modifier le code)

## Références

- **Planification :** [`EPIC05_PLAN.md`](./EPIC05_PLAN.md)
- **Audit sécurité :** [`SECURITY_AUDIT_EPIC05.md`](./SECURITY_AUDIT_EPIC05.md)
- **Backend README :** [`README.md`](./README.md)

## Exemple de flux complet

```bash
# 1. Login (génère un log "login")
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@wazash.io", "password": "dummy123"}'

# 2. POST event intrusion (génère un log "event_ingested" + alerte auto)
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion",
    "severity": "high",
    "details": {"source_ip": "192.168.1.100"}
  }'

# 3. Vérifier les logs d'audit (devrait contenir login + event_ingested + alert_generated)
curl -X GET http://localhost:8000/api/v1/audit/

# Exemple de sortie :
# [
#   {"id": "audit-003", "timestamp": "...", "action": "alert_generated", ...},
#   {"id": "audit-002", "timestamp": "...", "action": "event_ingested", ...},
#   {"id": "audit-001", "timestamp": "...", "action": "login", ...}
# ]
```

## Statut

✅ EPIC-05 terminé et testé (29 tests passés)
