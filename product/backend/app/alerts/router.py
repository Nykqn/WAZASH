"""Router pour la gestion des alertes."""

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.alerts.rules import match_rule
from app.alerts.schemas import AlertGenerateResponse
from app.core.database import get_db
from app.core.storage import add_alert, add_audit_log, get_alerts, get_events, seed_default_users
from app.events.schemas import EventPayload

router = APIRouter(tags=["alerts"])


@router.get("/")
async def list_alerts(
    db: Session = Depends(get_db),
    format: str = "json",
    severity: str | None = None,
    status: str | None = None,
):
    """Retourne la liste des alertes avec filtres optionnels."""
    seed_default_users(db)
    from app.models.alert import Alert
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.timestamp.desc()).all()

    if format == "csv":
        header = "id,event_id,rule_name,severity,timestamp,status,created_at\n"
        rows = ""
        for a in alerts:
            rows += f"{a.id},{a.event_id},{a.rule_name},{a.severity},{a.timestamp},{a.status},{a.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return alerts


@router.post("/generate")
async def generate_alert(payload: EventPayload, db: Session = Depends(get_db)) -> AlertGenerateResponse:
    seed_default_users(db)
    rule = match_rule(payload)

    if rule is None:
        return AlertGenerateResponse(
            status="no_match",
            message="Aucune règle ne correspond à cet événement",
        )

    events = get_events(db)
    event_id = len(events) + 1

    alert = add_alert(db, {
        "event_id": event_id,
        "rule_name": rule["rule_name"],
        "severity": rule["severity"],
        "timestamp": payload.timestamp,
        "status": "open",
    })
    add_audit_log(db, "alert_generated", None, f"Alerte {alert.rule_name} générée")

    return AlertGenerateResponse(
        status="generated",
        alert_id=alert.id,
        message=f"Alerte générée avec succès: {rule['rule_name']}",
    )
