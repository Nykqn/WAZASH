"""Router pour la gestion des alertes."""

from fastapi import APIRouter

from app.alerts.rules import match_rule
from app.alerts.schemas import Alert, AlertGenerateResponse
from app.core.storage import add_alert, get_alerts
from app.events.schemas import EventPayload

router = APIRouter(tags=["alerts"])


@router.get("/")
async def list_alerts() -> list[Alert]:
    """Retourne la liste de toutes les alertes générées."""
    return get_alerts()


@router.post("/generate")
async def generate_alert(payload: EventPayload) -> AlertGenerateResponse:
    """
    Force la génération d'une alerte à partir d'un payload d'événement.
    Utile pour les tests ou le déclenchement manuel.
    """
    rule = match_rule(payload)

    if rule is None:
        return AlertGenerateResponse(
            status="no_match",
            message="Aucune règle ne correspond à cet événement",
        )

    alert = Alert(
        id=0,  # Sera remplacé par add_alert
        event_id=len(get_alerts()) + 1,  # ID simple basé sur le nombre d'alertes
        rule_name=rule["rule_name"],
        severity=rule["severity"],
        timestamp=payload.timestamp,
        status="open",
    )

    alert = add_alert(alert)

    return AlertGenerateResponse(
        status="generated",
        alert_id=alert.id,
        message=f"Alerte générée avec succès: {rule['rule_name']}",
    )
