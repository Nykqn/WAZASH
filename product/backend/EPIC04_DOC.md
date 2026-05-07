# EPIC-04 : Documentation d'implémentation - Alertes Simples

**Date** : 2026-05-06
**Statut** : ✅ Implémenté et testé
**Références** :
- Planification : [`EPIC04_PLAN.md`](./EPIC04_PLAN.md)
- Audit sécurité : [`SECURITY_AUDIT_EPIC04.md`](./SECURITY_AUDIT_EPIC04.md)

## 1. Vue d'ensemble

L'EPIC-04 ajoute un système d'alertes simples au backend WAZASH. Ce système génère automatiquement des alertes basées sur les événements de sécurité ingérés via l'EPIC-02 (`POST /api/v1/events`).

## 2. Architecture

### 2.1 Structure des fichiers

```
app/alerts/
├── router.py      # Endpoints REST (GET /api/v1/alerts, POST /api/v1/alerts/generate)
├── schemas.py     # Schémas Pydantic (Alert, AlertGeneratePayload, AlertGenerateResponse)
└── rules.py       # Règles d'alerte simples

app/events/
└── router.py      # Modifié pour générer automatiquement une alerte après ingestion

app/core/
└── storage.py     # Ajout de alerts_store et fonctions associées
```

### 2.2 Schéma d'une alerte

```python
class Alert(BaseModel):
    id: str               # Identifiant unique (ex: alert-001)
    event_id: str         # Référence vers l'événement source
    rule_name: str        # Nom de la règle ayant déclenché l'alerte
    severity: str         # Sévérité (critical, high, medium, low)
    timestamp: datetime   # Date et heure de création
    status: str           # Statut (open, closed)
```

## 3. Règles d'alerte

Les règles sont définies dans `app/alerts/rules.py`. Actuellement, deux règles simples sont implémentées :

| Type d'événement (`event_type`) | Sévérité de l'alerte | Règle |
|--------------------------------|----------------------|-------|
| `intrusion`                    | `critical`           | Toute détection d'intrusion génère une alerte critique |
| `malware`                      | `high`               | Toute détection de malware génère une alerte de haute sévérité |
| Autres                          | -                    | Aucune alerte générée |

### Fonctionnement

```python
def evaluate_alert_rule(event: Event) -> Optional[Alert]:
    """
    Évalue si un événement doit générer une alerte selon les règles définies.
    Retourne une alerte si une règle match, sinon None.
    """
    if event.event_type == "intrusion":
        return Alert(
            id=f"alert-{uuid.uuid4().hex[:8]}",
            event_id=event.id,
            rule_name="intrusion_detected",
            severity="critical",
            timestamp=datetime.utcnow(),
            status="open"
        )
    elif event.event_type == "malware":
        return Alert(
            id=f"alert-{uuid.uuid4().hex[:8]}",
            event_id=event.id,
            rule_name="malware_detected",
            severity="high",
            timestamp=datetime.utcnow(),
            status="open"
        )
    return None
```

## 4. Endpoints

### 4.1 GET `/api/v1/alerts/`

Liste toutes les alertes générées, triées par timestamp décroissant.

**Réponse** :
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

### 4.2 POST `/api/v1/alerts/generate`

Génération manuelle d'une alerte à partir d'un événement existant.

**Payload** :
```json
{
  "event_id": "event-001"
}
```

**Réponse** :
```json
{
  "message": "Alert generated successfully",
  "alert": { ... }
}
```

### 4.3 Génération automatique (POST `/api/v1/events`)

Lors de l'ingestion d'un événement via `POST /api/v1/events`, si le `event_type` correspond à une règle, une alerte est automatiquement générée et stockée en mémoire.

## 5. Stockage

### 5.1 Stockage en mémoire

Les alertes sont stockées dans une liste Python simple (`alerts_store`) dans `app/core/storage.py`.

**Fonctions disponibles** :
- `add_alert(alert: Alert)` - Ajoute une alerte à la liste
- `get_alerts() -> List[Alert]` - Retourne toutes les alertes (triées par timestamp décroissant)
- `get_event_by_id(event_id: str) -> Optional[Event]` - Récupère un événement par son ID

### 5.2 Caractéristiques

- ✅ **Volatil** : Données perdues au redémarrage du serveur
- ✅ **Pas de persistance** : Aucune base de données, aucun fichier
- ✅ **Simple** : Adapté pour un MVP et des tests
- ✅ **Aucune dépendance externe** : Pas de Redis, pas de Celery, pas d'OpenAI

## 6. Tests

Le système d'alertes compte **8 tests** dans `tests/test_alerts.py` :

| Test | Description |
|------|-------------|
| `test_get_alerts_empty` | Vérifie que GET `/api/v1/alerts` retourne une liste vide initialement |
| `test_get_alerts_after_event` | Vérifie qu'une alerte est générée après POST `/api/v1/events` avec `intrusion` |
| `test_alert_generation_manual` | Vérifie la génération manuelle via POST `/api/v1/alerts/generate` |
| `test_alert_generation_event_not_found` | Vérifie la gestion d'erreur si l'event_id n'existe pas (404) |
| `test_alert_rule_intrusion_critical` | Vérifie que `intrusion` génère une alerte `critical` |
| `test_alert_rule_malware_high` | Vérifie que `malware` génère une alerte `high` |
| `test_alert_invalid_payload` | Vérifie la validation du payload (422 si champs invalides) |
| `test_alert_generate_invalid_payload` | Vérifie la validation du payload pour `/api/v1/alerts/generate` |

**Total du projet** : **24 tests** (16 existants + 8 alertes)

## 7. Limites et contraintes

### 7.1 Limites actuelles

1. **Stockage mémoire uniquement** :
   - Les alertes sont perdues au redémarrage
   - Pas de persistance sur disque ou base de données
   - Adapté pour un MVP, pas pour la production

2. **Pas de corrélation avancée** :
   - Les règles sont simples (match exact sur `event_type`)
   - Pas de corrélation entre plusieurs événements
   - Pas de détection de patterns complexes
   - Pas de machine learning ou d'IA

3. **Règles statiques** :
   - Les règles sont codées en dur dans `app/alerts/rules.py`
   - Pas de configuration dynamique des règles via API
   - Pas de règles personnalisables par l'utilisateur

4. **Gestion des statuts basique** :
   - Le statut est toujours `open` à la création
   - Pas d'endpoint pour mettre à jour le statut (TODO pour EPIC future)
   - Pas de gestion des faux positifs

### 7.2 Contraintes respectées

- ✅ Aucune base de données
- ✅ Aucun Redis
- ✅ Aucun Celery
- ✅ Aucun OpenAI
- ✅ Validation stricte des payloads (`extra='forbid'` sur tous les schémas Pydantic)
- ✅ Aucun secret exposé
- ✅ Tests complets (24 tests passés)

## 8. Exemples d'utilisation

### 8.1 Génération automatique d'alerte (intrusion)

```bash
# Étape 1 : Ingest un événement intrusion
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint_id": "ep-001",
    "timestamp": "2026-05-06T10:30:00",
    "event_type": "intrusion",
    "severity": "high",
    "details": {"source_ip": "192.168.1.100", "port": 22}
  }'

# Étape 2 : Vérifier que l'alerte a été générée
curl -X GET http://localhost:8000/api/v1/alerts/
```

### 8.2 Génération manuelle d'alerte

```bash
# Générer manuellement une alerte pour un événement existant
curl -X POST http://localhost:8000/api/v1/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "event-001"
  }'
```

### 8.3 Lister les alertes

```bash
# Récupérer toutes les alertes
curl -X GET http://localhost:8000/api/v1/alerts/

# Réponse attendue :
# [
#   {
#     "id": "alert-001",
#     "event_id": "event-001",
#     "rule_name": "intrusion_detected",
#     "severity": "critical",
#     "timestamp": "2026-05-06T10:30:00",
#     "status": "open"
#   }
# ]
```

## 9. Audit de sécurité

L'audit de sécurité (voir [`SECURITY_AUDIT_EPIC04.md`](./SECURITY_AUDIT_EPIC04.md)) a validé :

- ✅ Absence de secrets codés en dur
- ✅ Validation stricte des payloads (correction appliquée : `extra='forbid'`)
- ✅ Gestion correcte des erreurs (codes HTTP appropriés)
- ✅ Routes sécurisées et préfixées correctement
- ✅ Stockage mémoire sûr
- ✅ Conformité aux contraintes (pas de dépendances externes)
- ✅ 8 tests d'alertes passés avec succès

## 10. Prochaines étapes (futures EPICs)

- **Mise à jour du statut des alertes** : Endpoint `PATCH /api/v1/alerts/{id}` pour fermer une alerte
- **Règles dynamiques** : Configuration des règles via API ou fichier de configuration
- **Corrélation d'événements** : Détection de patterns basés sur plusieurs événements
- **Persistance** : Stockage des alertes dans une base de données (pour la production)
- **Notifications** : Envoi de notifications (email, webhook) lors de la génération d'alertes critiques

---

**Documentation générée par** : @devops-engineer
**Validation** : @project-manager-tech, @security-tech-lead
