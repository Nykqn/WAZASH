"""Schemas Pydantic pour les alertes."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Alert(BaseModel):
    """Schéma pour une alerte générée."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    rule_name: str
    severity: str
    timestamp: datetime
    status: str


class AlertGenerateResponse(BaseModel):
    """Schéma de réponse pour la génération d'alerte."""

    model_config = ConfigDict(extra="forbid")

    status: str
    alert_id: int | None = None
    message: str
