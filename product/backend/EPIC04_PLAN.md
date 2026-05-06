# EPIC-04 : Alertes Simples - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Priorité 7 (Alertes actionnables)

## 1. Objectif
Implémenter un système d'**alertes simples** basées sur les événements ingérés (EPIC-02). Génération d'alertes selon des règles simples, stockage en mémoire, et exposition via `GET /api/v1/alerts`.

## 2. User Story
- **US-04.1** : En tant que SOC, je consulte les alertes générées automatiquement à partir des événements reçus pour détecter des incidents.

## 3. Fichiers à créer/modifier
- `app/alerts/rules.py` : Règles simples (ex. `event_type == "intrusion" → alerte critique`)
- `app/alerts/schemas.py` : Schéma `Alert` (`id`, `event_id`, `rule_name`, `severity`, `timestamp`, `status`)
- `app/alerts/router.py` : POST `/api/v1/alerts/generate` + GET `/api/v1/alerts`
- `app/events/router.py` : Modification pour générer alerte après ingestion event
- `app/core/storage.py` : Ajout `alerts_store`
- `tests/test_alerts.py` : Tests (génération, lecture, règles)

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- POST `/api/v1/events` génère automatiquement une alerte si règle match
- GET `/api/v1/alerts` retourne la liste des alertes stockées
- Règles simples (ex: `intrusion` → `critical`, `malware` → `high`)
- Aucune base de données, Redis, Celery ou OpenAI
- Tous les tests pytest passent

## 6. Tests attendus
- `test_alert_generation_after_event` : POST event → alerte créée
- `test_get_alerts_empty` : GET alerts vide initialement
- `test_get_alerts_after_generation` : GET alerts retourne l'alerte
- `test_alert_rule_matching` : Vérifie que la règle s'applique correctement

## 7. Risques
- Couplage trop fort entre events et alerts
- Oubli de validation des alertes générées
- Sur-ingénierie des règles (rester simple)

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @backend-python-dev)
