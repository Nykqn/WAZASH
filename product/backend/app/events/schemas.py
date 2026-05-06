"""Schemas Pydantic pour les événements."""

from datetime import datetime

from pydantic import BaseModel


class EventPayload(BaseModel):
    """Payload pour un événement de sécurité."""

    endpoint_id: str
    timestamp: datetime
    event_type: str
    severity: str  # ex: "high", "medium", "low"
    details: dict
