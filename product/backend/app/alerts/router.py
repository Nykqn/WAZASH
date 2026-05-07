"""Router pour la gestion des alertes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.alerts.rules import match_rule
from app.alerts.schemas import AlertGenerateResponse, AlertUpdate, Alert as AlertSchema
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.storage import add_alert, add_audit_log, get_alerts, get_events, seed_default_users, update_alert_status
from app.events.schemas import EventPayload
from app.models.alert import Alert
from app.models.user import User

VALID_STATUSES = {"new", "in_review", "closed"}

router = APIRouter(tags=["alerts"])


@router.get("/")
async def list_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    format: str = "json",
    severity: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    """Retourne la liste des alertes avec filtres optionnels."""
    seed_default_users(db)
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.timestamp.desc()).offset(offset).limit(limit).all()

    if format == "csv":
        header = "id,event_id,rule_name,severity,timestamp,status,created_at\n"
        rows = ""
        for a in alerts:
            rows += f"{a.id},{a.event_id},{a.rule_name},{a.severity},{a.timestamp},{a.status},{a.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return alerts


@router.patch("/{alert_id}")
async def update_alert(
    alert_id: int,
    payload: AlertUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> AlertSchema:
    if payload.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"Statut invalide. Valeurs autorisées: {', '.join(sorted(VALID_STATUSES))}",
        )
    seed_default_users(db)
    alert = update_alert_status(db, alert_id, payload.status)
    if alert is None:
        raise HTTPException(status_code=404, detail=f"Alerte {alert_id} introuvable")
    add_audit_log(db, "alert_status_updated", None, f"Alerte {alert_id} → {payload.status}")
    return alert


@router.post("/generate")
async def generate_alert(payload: EventPayload, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> AlertGenerateResponse:
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
        "status": "new",
    })
    add_audit_log(db, "alert_generated", None, f"Alerte {alert.rule_name} générée")

    return AlertGenerateResponse(
        status="generated",
        alert_id=alert.id,
        message=f"Alerte générée avec succès: {rule['rule_name']}",
    )
