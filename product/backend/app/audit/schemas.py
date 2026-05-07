"""Schemas Pydantic pour l'audit."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLog(BaseModel):
    """Schema pour un log d'audit."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    action: str
    user_email: str | None = None
    details: str
