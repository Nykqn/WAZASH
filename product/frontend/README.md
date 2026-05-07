# WAZASH Frontend Dashboard

Dashboard web simple pour visualiser les données du backend WAZASH.

## Prérequis

- Backend WAZASH lancé sur `http://localhost:8000`
- Navigateur web moderne

## Lancement

1. Démarrer le backend :
   ```bash
   cd product/backend
   source .venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Ouvrir le dashboard :
   - Ouvrir le fichier `product/frontend/index.html` dans votre navigateur
   - Ou utiliser un serveur HTTP simple :
     ```bash
     cd product/frontend
     python3 -m http.server 8080
     ```
     Puis accéder à `http://localhost:8080`

## Fonctionnalités

- Connexion avec `admin@wazash.io` / `dummy123`
- Health check
- Envoi de heartbeats
- Envoi d'événements (déclenche alertes automatiquement)
- Visualisation des alertes
- Visualisation de l'audit trail

## Limitations (MVP)

- Pas de dashboard graphique avancé (graphiques, cartes)
- Pas d'inventaire d'actifs visuel
- Pas d'export CSV/JSON via l'interface
- Pas de gestion multi-utilisateurs

Ces fonctionnalités seront ajoutées dans les versions post-MVP.
