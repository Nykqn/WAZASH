"""Router pour l'ingestion d'événements."""

import json as _json

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.alerts.rules import match_rule
from app.core.database import get_db
from app.core.security import get_current_user, verify_agent_key
from app.core.storage import add_alert, add_audit_log, add_event, get_events, seed_default_users
from app.events.schemas import EventPayload
from app.models.event import Event
from app.models.user import User

router = APIRouter(tags=["events"])


@router.post("/events")
async def receive_event(payload: EventPayload, db: Session = Depends(get_db), _: bool = Depends(verify_agent_key)) -> dict[str, str]:
    seed_default_users(db)
    add_event(db, payload.model_dump())
    add_audit_log(db, "event_ingested", None, f"Événement {payload.event_type} ingéré")

    rule = match_rule(payload)
    if rule is not None:
        events = get_events(db)
        event_id = len(events)
        add_alert(db, {
            "event_id": event_id,
            "rule_name": rule["rule_name"],
            "severity": rule["severity"],
            "timestamp": payload.timestamp,
            "status": "open",
        })

    return {"status": "ok"}


@router.get("/events")
async def list_events(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    format: str = "json",
    event_type: str | None = None,
    severity: str | None = None,
    endpoint_id: str | None = None,
):
    """Retourne la liste des événements avec filtres optionnels."""
    seed_default_users(db)
    query = db.query(Event)
    if endpoint_id:
        query = query.filter(Event.endpoint_id == endpoint_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if severity:
        query = query.filter(Event.severity == severity)
    events = query.order_by(Event.timestamp.desc()).all()

    if format == "csv":
        header = "id,endpoint_id,timestamp,event_type,severity,details,created_at\n"
        rows = ""
        for ev in events:
            details = _json.dumps(ev.details).replace(",", ";").replace("\n", " ")
            rows += f"{ev.id},{ev.endpoint_id},{ev.timestamp},{ev.event_type},{ev.severity},{details},{ev.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return events
