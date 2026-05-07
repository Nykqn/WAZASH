from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AssetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    endpoint_id: str
    hostname: str | None = None
    ip_address: str | None = None
    os: str | None = None


class AssetUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hostname: str | None = None
    ip_address: str | None = None
    os: str | None = None
    status: str | None = None


class Asset(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    endpoint_id: str
    hostname: str | None = None
    ip_address: str | None = None
    os: str | None = None
    status: str
    last_seen: datetime | None = None
    created_at: datetime
    updated_at: datetime
