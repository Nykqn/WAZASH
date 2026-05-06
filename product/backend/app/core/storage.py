"""Stockage en mémoire pour les heartbeats, événements et alertes."""

from typing import Any

from app.alerts.schemas import Alert

# Stockage en mémoire (listes simples)
heartbeats_store: list[dict[str, Any]] = []
events_store: list[dict[str, Any]] = []
alerts_store: list[Alert] = []

# Compteur pour générer des IDs uniques
alert_id_counter: int = 0


def add_heartbeat(heartbeat: dict[str, Any]) -> None:
    """Ajoute un heartbeat au stockage en mémoire."""
    heartbeats_store.append(heartbeat)


def add_event(event: dict[str, Any]) -> None:
    """Ajoute un événement au stockage en mémoire."""
    events_store.append(event)


def get_heartbeats() -> list[dict[str, Any]]:
    """Retourne tous les heartbeats stockés."""
    return heartbeats_store


def get_events() -> list[dict[str, Any]]:
    """Retourne tous les événements stockés."""
    return events_store


def add_alert(alert: Alert) -> Alert:
    """Ajoute une alerte au stockage en mémoire."""
    global alert_id_counter
    alert_id_counter += 1
    alert.id = alert_id_counter
    alerts_store.append(alert)
    return alert


def get_alerts() -> list[Alert]:
    """Retourne toutes les alertes stockées."""
    return alerts_store
