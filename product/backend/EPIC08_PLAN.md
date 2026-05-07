# EPIC-08 : Inventaire d'actifs + Auto-registration - Planification

**Date** : 2026-05-06
**Étape** : 1. Planification (Validée par @project-manager-tech)
**Lien MVP** : Inventaire d'actifs (auto-découverte via heartbeat)

## 1. Objectif
Implémenter un inventaire d'actifs avec CRUD complet, auto-enregistrement automatique des endpoints à la réception d'un heartbeat, et exposition via API REST.

## 2. User Story
- **US-08.1** : En tant que SOC, je consulte et gère l'inventaire des actifs (endpoints) pour connaître l'état de mon parc.
- **US-08.2** : En tant que SOC, un endpoint inconnu qui envoie un heartbeat est automatiquement ajouté à l'inventaire.

## 3. Fichiers à créer/modifier
- `app/models/asset.py` : Modèle SQLAlchemy Asset (endpoint_id, hostname, ip_address, os, status, last_seen)
- `app/assets/schemas.py` : Schémas Pydantic (AssetCreate, AssetUpdate, Asset)
- `app/assets/router.py` : CRUD complet (GET/POST/PATCH/DELETE /api/v1/assets/)
- `app/heartbeat/router.py` : Modification pour auto-registrer l'endpoint
- `app/core/storage.py` : Fonctions CRUD Asset (add_asset, get_asset, update_asset, delete_asset)
- `app/main.py` : Inclusion du router assets
- `tests/test_assets.py` : Tests CRUD + auto-registration + CSV

## 4. Agents responsables
- **Développement** : @backend-python-dev
- **Tests** : @qa-tester
- **Audit sécurité** : @security-tech-lead
- **Documentation** : @devops-engineer

## 5. Critères d'acceptation
- POST `/api/v1/assets/` crée un asset (201) avec endpoint_id unique
- GET `/api/v1/assets/` liste tous les assets (200)
- GET `/api/v1/assets/{endpoint_id}` retourne un asset spécifique (200)
- PATCH `/api/v1/assets/{endpoint_id}` met à jour un asset (200)
- DELETE `/api/v1/assets/{endpoint_id}` supprime un asset (204)
- Doublon d'endpoint_id retourne 409
- Asset inexistant retourne 404
- Heartbeat d'un endpoint inconnu crée automatiquement l'asset
- Export CSV disponible via `?format=csv`
- Tous les tests pytest passent

## 6. Tests attendus
- `test_list_assets_empty` : GET liste vide initialement
- `test_create_asset` : POST crée un asset (201)
- `test_create_asset_duplicate` : POST doublon (409)
- `test_get_asset` : GET par endpoint_id (200)
- `test_get_asset_not_found` : GET inexistant (404)
- `test_update_asset` : PATCH modifie champs (200)
- `test_delete_asset` : DELETE supprime (204)
- `test_list_assets_csv` : Export CSV (200)
- `test_heartbeat_auto_registers_asset` : Heartbeat → création auto

## 7. Risques
- Conflit de création si deux heartbeats simultanés pour le même endpoint
- Oubli de validation Pydantic sur les payloads de création/mise à jour
- Pas de protection par authentification (acceptable pour MVP)

## 8. Validation
✅ Plan validé par @project-manager-tech
✅ Prêt pour l'étape 2 (Développement par @backend-python-dev)
