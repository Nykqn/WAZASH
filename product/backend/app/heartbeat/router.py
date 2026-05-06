"""Router pour l'ingestion de heartbeats."""

from fastapi import APIRouter

from app.core.storage import add_heartbeat
from app.heartbeat.schemas import HeartbeatPayload

router = APIRouter(tags=["heartbeat"])


@router.post("/heartbeat")
async def receive_heartbeat(payload: HeartbeatPayload) -> dict[str, str]:
    """Reçoit et stocke un heartbeat d'endpoint."""
    add_heartbeat(payload.model_dump())
    return {"status": "ok"}
