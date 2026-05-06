"""Schemas Pydantic pour l'authentification."""

from pydantic import BaseModel


class LoginPayload(BaseModel):
    """Payload pour la connexion utilisateur."""

    email: str
    password: str
