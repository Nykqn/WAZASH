# EPIC-05 : Audit Trail - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Priorité 8 (Audit Trail)

## 1. Objectif
Implémenter un système d'**audit trail** pour tracer les actions importantes (connexions, ingestion d'événements, génération d'alertes) avec stockage en mémoire et exposition via `GET /api/v1/audit`.

## 2. User Story
- **US-05.1** : En tant qu'administrateur SOC, je consulte les logs d'audit pour tracer qui a fait quoi et détecter des activités suspectes.

## 3. Fichiers à créer/modifier
- `app/audit/schemas.py` : Schéma `AuditLog` (`id`, `timestamp`, `action`, `user_email`, `details`)
- `app/audit/router.py` : GET `/api/v1/audit`
- `app/core/storage.py` : Ajout `audit_store`, `add_audit_log()`
- `app/auth/router.py` : Ajout audit log à la connexion
- `app/events/router.py` : Ajout audit log à l'ingestion
- `app/alerts/router.py` : Ajout audit log à la génération
- `tests/test_audit.py` : Tests (consultation, génération automatique)

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- Actions (login, event, alert) génèrent automatiquement des audit logs
- GET `/api/v1/audit` retourne la liste des logs par ordre chronologique
- Stockage en mémoire uniquement
- Aucune base de données, Redis, Celery ou OpenAI
- Tous les tests pytest passent

## 6. Tests attendus
- `test_get_audit_empty` : GET audit vide initialement
- `test_audit_after_login` : Connexion génère un log d'audit
- `test_audit_after_event` : Ingestion événement génère un log
- `test_audit_after_alert_generate` : Génération alerte génère un log
- `test_audit_order` : Vérifie l'ordre chronologique

## 7. Risques
- Sur-ingénierie (rester simple, pas de rotation des logs)
- Oubli d'ajouter l'audit dans certains endpoints
- Fuites d'informations sensibles dans les logs

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @backend-python-dev)
