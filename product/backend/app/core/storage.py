"""Stockage en mémoire pour les heartbeats et événements."""

from typing import Any

# Stockage en mémoire (listes simples)
heartbeats_store: list[dict[str, Any]] = []
events_store: list[dict[str, Any]] = []


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
