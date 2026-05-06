"""Tests pour l'ingestion d'événements."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.core.storage import events_store, get_events
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    """Vide le stockage avant chaque test."""
    events_store.clear()


def test_event_valid_payload() -> None:
    """Teste l'ingestion d'un événement avec un payload valide."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100", "port": 22},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_event_invalid_payload_missing_field() -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion_detected",
        # severity manquant
        "details": {},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 422


def test_event_invalid_payload_wrong_type() -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": "not_a_dict",  # devrait être un dict
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 422


def test_event_storage() -> None:
    """Teste que l'événement est bien stocké en mémoire."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100"},
    }
    client.post("/api/v1/events", json=payload)

    events = get_events()
    assert len(events) == 1
    assert events[0]["endpoint_id"] == "ep-001"
    assert events[0]["event_type"] == "intrusion_detected"
    assert events[0]["severity"] == "high"
    assert events[0]["details"]["source_ip"] == "192.168.1.100"


def test_event_multiple_storage() -> None:
    """Teste le stockage de plusieurs événements."""
    for i in range(3):
        payload = {
            "endpoint_id": f"ep-{i:03d}",
            "timestamp": datetime.now().isoformat(),
            "event_type": "test_event",
            "severity": "low",
            "details": {"index": i},
        }
        client.post("/api/v1/events", json=payload)

    events = get_events()
    assert len(events) == 3
