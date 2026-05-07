# EPIC-03 : Authentification JWT + bcrypt + RBAC - Documentation

**Date** : 2026-05-06 (mis à jour)
**Statut** : ✅ Implémenté et testé (avec évolutions post-skeleton)
**Références** :
- Planification : [`EPIC03_PLAN.md`](./EPIC03_PLAN.md)
- Audit sécurité : [`SECURITY_AUDIT_EPIC03.md`](./SECURITY_AUDIT_EPIC03.md)

## 1. Vue d'ensemble

L'EPIC-03 a évolué depuis le skeleton initial vers un système d'authentification complet avec JWT (JSON Web Tokens), bcrypt pour le hachage des mots de passe, et RBAC (Role-Based Access Control) basique.

## 2. Architecture

### 2.1 Structure des fichiers

```
app/core/
└── security.py     # Hachage bcrypt, création/décodage JWT, dépendances auth

app/auth/
├── router.py       # POST /api/v1/auth/login
└── schemas.py      # LoginPayload, TokenResponse

app/models/
└── user.py         # Modèle SQLAlchemy User (email, hashed_password, role, is_active)

app/core/
└── storage.py      # get_user_by_email, create_user, seed_default_users
```

### 2.2 Flux d'authentification

```
Client                    Backend                    Database
  │                         │                          │
  │  POST /auth/login       │                          │
  │  {email, password}      │                          │
  │────────────────────────▶│                          │
  │                         │  seed_default_users()    │
  │                         │  ───────────────────────▶│
  │                         │  get_user_by_email()     │
  │                         │  ───────────────────────▶│
  │                         │                          │
  │                         │  verify_password()       │
  │                         │  (bcrypt)                │
  │                         │                          │
  │                         │  create_access_token()   │
  │                         │  (JWT)                   │
  │                         │                          │
  │  {access_token, bearer} │                          │
  │◀────────────────────────│                          │
```

## 3. Implémentation

### 3.1 Hachage des mots de passe (bcrypt)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 3.2 JSON Web Tokens (JWT)

```python
from jose import jwt

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    except JWTError:
        return {}
```

### 3.3 Dépendances FastAPI

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Décode le token, vérifie l'utilisateur dans la DB
    ...

def require_role(role: str):
    # Vérifie que l'utilisateur a le rôle requis (ou est admin)
    ...
```

### 3.4 Modèle utilisateur

```python
class User(Base):
    __tablename__ = "users"
    id: int
    email: str              # Unique, indexé
    hashed_password: str    # Hash bcrypt
    role: str               # "admin" ou "analyst"
    is_active: bool         # True par défaut
    created_at: datetime
```

### 3.5 Utilisateurs par défaut

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| `admin@wazash.io` | `dummy123` | `admin` |
| `user@wazash.io` | `test456` | `analyst` |

Les utilisateurs sont créés automatiquement au premier appel (`seed_default_users()`).

## 4. Endpoint

### POST `/api/v1/auth/login`

**Payload :**
```json
{
  "email": "admin@wazash.io",
  "password": "dummy123"
}
```

**Réponse (200) :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Codes d'erreur :**
- 401 : Identifiants invalides
- 403 : Compte désactivé
- 422 : Payload invalide

## 5. RBAC (Role-Based Access Control)

La fonction `require_role(role)` est disponible pour protéger les endpoints :

```python
from app.core.security import require_role

@router.get("/admin-only")
async def admin_endpoint(current_user: User = Depends(require_role("admin"))):
    ...
```

- Un utilisateur avec le rôle `admin` a accès à tout
- Un utilisateur avec le rôle `analyst` a accès uniquement aux endpoints marqués pour son rôle
- Les routes actuelles n'utilisent pas encore `require_role` (MVP)

## 6. Audit trail

Chaque connexion réussie génère un log d'audit :
```python
add_audit_log(db, "login", user.email, f"Connexion réussie pour {user.email}")
```

## 7. Tests (6 tests)

| Test | Description |
|------|-------------|
| `test_login_valid` | Login admin réussi (200 + JWT) |
| `test_login_invalid` | Mauvais mot de passe (401) |
| `test_login_invalid_payload_missing_field` | Champ manquant (422) |
| `test_login_invalid_payload_wrong_type` | Type invalide (422) |
| `test_login_unknown_user` | Utilisateur inexistant (401) |
| `test_login_user_analyst` | Login analyst réussi (200) |

## 8. Sécurité

- ✅ Mots de passe hachés avec bcrypt (jamais en clair)
- ✅ Tokens JWT avec expiration (30 minutes par défaut)
- ✅ Validation Pydantic stricte (`extra='forbid'`)
- ✅ Aucun secret réel dans le code
- ✅ Messages d'erreur génériques (pas de fuite d'information)
- ✅ Comptes désactivés bloqués (is_active=False)

## 9. Limites

1. **Clé JWT en dur** dans `config.py` pour le développement (à changer via `.env` en production)
2. **Pas de refresh token** (le token expire après 30 min, reconnexion nécessaire)
3. **Pas de rate limiting** sur le login (risque de brute-force en production)
4. **Pas d'inscription utilisateur** via API (utilisateurs seed uniquement)

---

**Validation** : @project-manager-tech, @security-tech-lead
