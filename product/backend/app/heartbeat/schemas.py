"""Schemas Pydantic pour les heartbeats."""

from datetime import datetime

from pydantic import BaseModel


class HeartbeatPayload(BaseModel):
    """Payload pour un heartbeat d'endpoint."""

    endpoint_id: str
    timestamp: datetime
    status: str  # ex: "up", "down"
