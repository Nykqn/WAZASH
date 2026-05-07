"""Règles de génération d'alertes basées sur les événements."""

from typing import Optional

from app.events.schemas import EventPayload


def match_rule(event: EventPayload) -> Optional[dict]:
    """
    Applique des règles simples sur un événement.

    Returns:
        Un dictionnaire avec rule_name et severity si une règle match, None sinon.
    """
    if event.event_type == "intrusion":
        return {"rule_name": "intrusion_detected", "severity": "critical"}
    elif event.event_type == "malware":
        return {"rule_name": "malware_detected", "severity": "high"}
    else:
        return None
