# EPIC-08 : Inventaire d'actifs + Auto-registration - Documentation

**Date** : 2026-05-06
**Statut** : ✅ Implémenté et testé
**Références** :
- Planification : [`EPIC08_PLAN.md`](./EPIC08_PLAN.md)
- Audit sécurité : [`SECURITY_AUDIT_EPIC08.md`](./SECURITY_AUDIT_EPIC08.md)

## 1. Vue d'ensemble

L'EPIC-08 ajoute un système d'inventaire d'actifs (assets) au backend WAZASH. Chaque endpoint qui envoie un heartbeat est automatiquement enregistré comme actif. Le SOC peut également créer, lire, mettre à jour et supprimer des actifs via l'API REST.

## 2. Architecture

### 2.1 Structure des fichiers

```
app/assets/
├── router.py      # Endpoints REST (GET/POST/PATCH/DELETE /api/v1/assets/)
└── schemas.py     # Schémas Pydantic (AssetCreate, AssetUpdate, Asset)

app/models/
└── asset.py       # Modèle SQLAlchemy Asset

app/heartbeat/
└── router.py      # Modifié : auto_register_asset() à chaque heartbeat
```

### 2.2 Modèle de données

```python
class Asset(Base):
    __tablename__ = "assets"
    id: int              # Identifiant unique (auto-incrémenté)
    endpoint_id: str     # Identifiant de l'endpoint (unique, indexé)
    hostname: str | None # Nom d'hôte
    ip_address: str | None # Adresse IP
    os: str | None       # Système d'exploitation
    status: str          # Statut : "active", "inactive", "down"
    last_seen: datetime  # Dernier heartbeat reçu
    created_at: datetime # Date de création
    updated_at: datetime # Date de dernière modification
```

### 2.3 Auto-registration

À chaque heartbeat reçu via `POST /api/v1/heartbeat`, la fonction `auto_register_asset()` vérifie si l'`endpoint_id` existe déjà dans la table `assets`. Si ce n'est pas le cas, un nouvel asset est créé automatiquement avec le statut `"active"`.

```python
def auto_register_asset(db: Session, endpoint_id: str) -> None:
    existing = db.query(Asset).filter(Asset.endpoint_id == endpoint_id).first()
    if not existing:
        asset = Asset(endpoint_id=endpoint_id, status="active")
        db.add(asset)
        db.commit()
```

Le heartbeat met également à jour `last_seen` et `status` de l'asset correspondant.

## 3. Endpoints

### 3.1 GET `/api/v1/assets/`
Liste tous les actifs, triés par `updated_at` décroissant.

**Paramètres optionnels :**
- `format` : `"json"` (défaut) ou `"csv"`
- `status_filter` : Filtre par statut (`"active"`, `"inactive"`, `"down"`)

**Exemple de réponse :**
```json
[
  {
    "id": 1,
    "endpoint_id": "ep-web-01",
    "hostname": "srv-web-01",
    "ip_address": "192.168.1.10",
    "os": "Ubuntu 22.04",
    "status": "active",
    "last_seen": "2026-05-06T10:30:00",
    "created_at": "2026-05-06T10:30:00",
    "updated_at": "2026-05-06T10:30:00"
  }
]
```

### 3.2 POST `/api/v1/assets/`
Crée un nouvel asset.

**Payload (`AssetCreate`) :**
```json
{
  "endpoint_id": "ep-001",
  "hostname": "srv-web-01",
  "ip_address": "192.168.1.10",
  "os": "Ubuntu 22.04"
}
```

**Codes retour :** 201 (créé), 409 (doublon), 422 (payload invalide)

### 3.3 GET `/api/v1/assets/{endpoint_id}`
Retourne un asset spécifique par son `endpoint_id`.

**Codes retour :** 200 (succès), 404 (non trouvé)

### 3.4 PATCH `/api/v1/assets/{endpoint_id}`
Met à jour partiellement un asset.

**Payload (`AssetUpdate`) :**
```json
{
  "hostname": "new-hostname",
  "status": "inactive"
}
```

**Codes retour :** 200 (succès), 404 (non trouvé), 422 (payload invalide)

### 3.5 DELETE `/api/v1/assets/{endpoint_id}`
Supprime un asset.

**Codes retour :** 204 (succès), 404 (non trouvé)

## 4. Audit trail

Les actions suivantes sur les assets génèrent automatiquement des logs d'audit :
- `asset_created` : Création d'un asset
- `asset_updated` : Modification d'un asset
- `asset_deleted` : Suppression d'un asset

## 5. Tests

L'EPIC-08 ajoute **9 tests** dans `tests/test_assets.py` :

| Test | Description |
|------|-------------|
| `test_list_assets_empty` | Vérifie que GET retourne une liste vide initialement |
| `test_create_asset` | Vérifie la création d'un asset (201) |
| `test_create_asset_duplicate` | Vérifie le rejet d'un doublon (409) |
| `test_get_asset` | Vérifie la lecture par endpoint_id (200) |
| `test_get_asset_not_found` | Vérifie 404 pour asset inexistant |
| `test_update_asset` | Vérifie la mise à jour partielle (200) |
| `test_delete_asset` | Vérifie la suppression (204) |
| `test_list_assets_csv` | Vérifie l'export CSV |
| `test_heartbeat_auto_registers_asset` | Vérifie qu'un heartbeat crée automatiquement l'asset |

## 6. Limites et contraintes

### 6.1 Limites actuelles
1. **Pas d'authentification** sur les routes assets (acceptable pour MVP)
2. **Pas de pagination** sur GET `/api/v1/assets/`
3. **Auto-registration basique** : pas de vérification de l'identité de l'endpoint
4. **Pas de champ tags/catégories** pour organiser les actifs

### 6.2 Contraintes respectées
- ✅ Validation stricte des payloads (`extra='forbid'`)
- ✅ Audit trail pour toutes les actions CRUD
- ✅ Aucun secret exposé
- ✅ Tests complets (9 tests)
- ✅ Export CSV disponible

---

**Validation** : @project-manager-tech, @security-tech-lead
