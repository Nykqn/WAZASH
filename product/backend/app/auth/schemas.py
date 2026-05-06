"""Schemas Pydantic pour l'authentification."""

from pydantic import BaseModel, ConfigDict


class LoginPayload(BaseModel):
    """Payload pour la connexion utilisateur."""

    model_config = ConfigDict(extra="forbid")

    email: str
    password: str
