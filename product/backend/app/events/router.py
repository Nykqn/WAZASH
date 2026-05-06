"""Router pour l'ingestion d'événements."""

from fastapi import APIRouter

from app.alerts.rules import match_rule
from app.alerts.schemas import Alert
from app.core.storage import add_alert, add_event, get_events
from app.events.schemas import EventPayload

router = APIRouter(tags=["events"])


@router.post("/events")
async def receive_event(payload: EventPayload) -> dict[str, str]:
    """Reçoit et stocke un événement de sécurité, génère une alerte si une règle match."""
    add_event(payload.model_dump())

    # Vérifier si une règle d'alerte s'applique
    rule = match_rule(payload)
    if rule is not None:
        # Utiliser le nombre d'événements comme référence pour event_id
        event_id = len(get_events())
        alert = Alert(
            id=0,  # Sera remplacé par add_alert
            event_id=event_id,
            rule_name=rule["rule_name"],
            severity=rule["severity"],
            timestamp=payload.timestamp,
            status="open",
        )
        add_alert(alert)

    return {"status": "ok"}
