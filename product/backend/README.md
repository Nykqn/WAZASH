# WAZASH Backend

Backend FastAPI pour l'application WAZASH.

## Prérequis

- Python 3.11 ou supérieur
- pip

## Installation et configuration

### 1. Créer l'environnement virtuel

```bash
cd product/backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -e ".[dev]"
```

Ou en une seule commande :

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

### 3. Configuration des variables d'environnement

Copier le fichier d'exemple et l'adapter si nécessaire :

```bash
cp .env.example .env
```

Les variables disponibles sont documentées dans `.env.example`.

## Lancement de l'application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API est accessible sur :
- http://localhost:8000 (API principale)
- http://localhost:8000/docs (Documentation Swagger UI)
- http://localhost:8000/redoc (Documentation ReDoc)

## Tests

Exécuter tous les tests avec pytest :

```bash
pytest -v
```

## Structure du projet

```
product/backend/
├── app/
│   ├── core/
│   │   └── config.py      # Configuration centralisée
│   ├── auth/
│   │   └── router.py      # Routes d'authentification
│   ├── health/
│   │   └── router.py      # Route de health check
│   └── main.py            # Point d'entrée FastAPI
├── tests/                 # Tests pytest
├── pyproject.toml         # Configuration du projet et dépendances
├── .env.example           # Exemple de variables d'environnement
└── README.md              # Ce fichier
```

## Dépannage

### Le port 8000 est déjà utilisé

Modifier le port dans la commande de lancement :

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Problème avec l'environnement virtuel

Supprimer et recréer l'environnement :

```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
