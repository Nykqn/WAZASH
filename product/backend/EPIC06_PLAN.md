# EPIC-06 : Docker Compose - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Priorité 9 (Docker Compose)

## 1. Objectif
Préparer **Docker Compose** pour lancer le backend WAZASH avec un environnement reproductible, incluant `Dockerfile`, `docker-compose.yml`, et `.dockerignore`.

## 2. User Story
- **US-06.1** : En tant que développeur, je lance l'application WAZASH avec `docker compose up` et je peux tester les endpoints.

## 3. Fichiers à créer/modifier
- `Dockerfile` (Image Python avec venv et dépendances)
- `docker-compose.yml` (Service `wazash-backend` sur port 8000)
- `.dockerignore` (Exclure `.venv`, `__pycache__`, `.env`)
- `.env.example` (Vérifier qu'il est documenté pour Docker)
- `README.md` (Mettre à jour avec commandes Docker)

## 4. Agents responsables
- **Développement** : @devops-engineer (Docker selon AGENTS.md)
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- `docker compose up` lance le backend sans erreur
- `GET /health` accessible sur `http://localhost:8000/health`
- Aucun secret dans l'image Docker (`.dockerignore` exclut `.env`)
- `pytest` passe dans le conteneur
- Image basée sur `python:3.11-slim` (légère)

## 6. Tests attendus
- `docker compose up -d` démarre sans erreur
- `curl http://localhost:8000/health` retourne 200
- `docker compose exec wazash-backend pytest -v` passe (29 tests)

## 7. Risques
- Port 8000 déjà utilisé
- Oubli de `.dockerignore` (fuite de `.env`)
- Dépendances manquantes dans Dockerfile
- Conflit entre `pyproject.toml` et l'installation Docker

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @devops-engineer)
