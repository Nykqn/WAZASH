# EPIC-03 : Authentification Utilisateur (US-01.1) - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Priorité 6 (Auth Agent)

## 1. Objectif
Implémenter le **skeleton** de l'authentification utilisateur (POST `/auth/login`) sans base de données, avec validation Pydantic, stockage en mémoire de utilisateurs fictifs, et tests associés.

## 2. User Story
- **US-01.1** : En tant qu'utilisateur SOC, je m'authentifie via `POST /api/v1/auth/login` avec email/mot de passe pour obtenir un token d'accès fictif.

## 3. Fichiers à créer/modifier
- `app/auth/schemas.py` : Schéma Pydantic `LoginPayload` (`email: str`, `password: str`)
- `app/auth/router.py` : Ajout de `POST /login` avec validation, stockage mémoire fictif
- `app/core/config.py` : Ajout de `SECRET_KEY` fictif pour skeleton (pas de valeur réelle)
- `tests/test_auth.py` : Tests (login valide, invalide, payload invalide)
- `.env.example` : Ajout de `SECRET_KEY` commenté

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- `POST /api/v1/auth/login` retourne 200 + token fictif pour identifiants valides
- Identifiants invalides retournent 401
- Payload invalide retourne 422 (validation Pydantic)
- Aucune base de données, Redis, Celery, OpenAI
- Aucun secret réel (`SECRET_KEY` fictif documenté dans `.env.example`)
- Tous les tests pytest passent

## 6. Tests attendus
- `test_login_valid` : 200 + token présent
- `test_login_invalid` : 401
- `test_login_invalid_payload` : 422

## 7. Risques
- Utilisation accidentelle de vrais secrets
- Sur-ingénierie (éviter JWT complet pour le skeleton)
- Oubli de validation Pydantic

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @backend-python-dev)
