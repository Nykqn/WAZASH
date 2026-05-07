from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CorrelationGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    correlation_type: str
    source_ip: str
    target_ip: str | None = None
    event_type: str | None = None
    window_start: datetime
    window_end: datetime
    event_count: int
    created_at: datetime
