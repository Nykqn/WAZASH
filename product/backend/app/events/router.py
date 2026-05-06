"""Router pour l'ingestion d'événements."""

from fastapi import APIRouter

from app.core.storage import add_event
from app.events.schemas import EventPayload

router = APIRouter(tags=["events"])


@router.post("/events")
async def receive_event(payload: EventPayload) -> dict[str, str]:
    """Reçoit et stocke un événement de sécurité."""
    add_event(payload.model_dump())
    return {"status": "ok"}
