"""Router pour l'authentification."""

from fastapi import APIRouter, HTTPException, status

from app.auth.schemas import LoginPayload
from app.core.storage import add_audit_log

router = APIRouter(prefix="/auth", tags=["auth"])

# Stockage en mémoire fictif (skeleton - pas de base de données)
_FAKE_USERS = {
    "admin@wazash.io": "dummy123",
    "user@wazash.io": "test456",
}


@router.post("/login")
def login(payload: LoginPayload) -> dict:
    """
    Authentifie un utilisateur et retourne un token d'accès fictif.

    - **email** : Adresse email de l'utilisateur
    - **password** : Mot de passe
    """
    stored_password = _FAKE_USERS.get(payload.email)

    if stored_password is None or stored_password != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    add_audit_log("login", payload.email, f"Connexion réussie pour {payload.email}")

    return {
        "access_token": "dummy-token-123",
        "token_type": "bearer",
    }
