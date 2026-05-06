"""Schemas Pydantic pour les heartbeats."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HeartbeatPayload(BaseModel):
    """Payload pour un heartbeat d'endpoint."""

    model_config = ConfigDict(extra="forbid")

    endpoint_id: str
    timestamp: datetime
    status: str  # ex: "up", "down"
