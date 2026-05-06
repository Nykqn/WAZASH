"""Schemas Pydantic pour les événements."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventPayload(BaseModel):
    """Payload pour un événement de sécurité."""

    model_config = ConfigDict(extra="forbid")

    endpoint_id: str
    timestamp: datetime
    event_type: str
    severity: str  # ex: "high", "medium", "low"
    details: dict
