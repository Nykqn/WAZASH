"""Schemas Pydantic pour l'authentification."""

from pydantic import BaseModel, ConfigDict


class LoginPayload(BaseModel):
    """Payload pour la connexion utilisateur."""

    model_config = ConfigDict(extra="forbid")

    email: str
    password: str


class TokenResponse(BaseModel):
    """Réponse après connexion réussie."""

    access_token: str
    token_type: str
    expires_in: int = 1800  # 30 minutes default
