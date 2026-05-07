# Rapport d'audit sécurité - EPIC-09 (GET endpoints + exports + frontend)

**Date** : 2026-05-06
**Auditeur** : @security-tech-lead
**Epic concerné** : EPIC-09 (GET endpoints, exports CSV, frontend SOC)
**Statut** : ✅ OK avec réserves

## Vérifications effectuées

### 1. Absence de secrets
✅ **Conforme** - Aucun secret codé en dur dans les GET endpoints, exports CSV ou frontend.
⚠️ **URL backend exposée** : `192.168.1.31:8000` en dur dans `app.js` (acceptable pour lab local).

### 2. Routes GET non sensibles
✅ **Conforme** - Les GET endpoints retournent uniquement des données opérationnelles (heartbeats, events, alerts, audit, assets).
✅ Aucune donnée sensible (mots de passe, tokens) exposée via les GET endpoints.

### 3. Exports CSV sécurisés
✅ **Conforme** - Les exports CSV utilisent les mêmes données que les réponses JSON.
✅ Aucune donnée supplémentaire ou sensible dans les exports CSV.
✅ Content-Type correct (`text/csv`).

### 4. Frontend sécurisé
✅ **Conforme** - Le frontend est servi par Nginx, pas d'exécution côté serveur.
✅ Le token JWT est stocké dans `localStorage` (standard pour SPA).
✅ Le frontend gère les erreurs 401 et déconnecte l'utilisateur.
⚠️ **Pas de HTTPS** (acceptable pour lab local).
⚠️ **Pas de protection CSRF** (acceptable pour MVP, le token est dans le header).

### 5. CORS configuré
✅ **Conforme** - CORS middleware configuré dans `app/main.py` avec `allow_origins=["http://192.168.1.31:8080"]`.
⚠️ Origine CORS spécifique à un environnement de lab (à adapter en production).

### 6. Filtres GET sécurisés
✅ **Conforme** - Les paramètres de filtre sont des chaînes simples, pas d'injection SQL possible (SQLAlchemy paramétré).
✅ Les filtres sont optionnels et validés implicitement par le typage Python.

### 7. Tests audités
✅ **Conforme** - 11 tests `test_exports.py` couvrant les formats JSON, CSV et les filtres.

## Réserves

1. ⚠️ **GET endpoints non authentifiés** : Tous les GET endpoints sont accessibles sans token (acceptable pour MVP).
2. ⚠️ **URL backend en dur** : L'URL `192.168.1.31:8000` est codée en dur dans le frontend.
3. ⚠️ **Pas de rate limiting** : Les GET endpoints peuvent être appelés sans limitation.

## Recommandations

- Rendre l'URL backend configurable via variable d'environnement dans le frontend
- Ajouter une authentification optionnelle sur les GET endpoints pour la production
- Implémenter une pagination pour éviter les timeouts sur gros volumes

## Conclusion

L'EPIC-09 est **fonctionnel et sécurisé** pour le MVP. Les réserves sont documentées et acceptables pour un environnement de lab.
