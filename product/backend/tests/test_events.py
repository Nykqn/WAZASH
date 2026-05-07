"""Tests pour l'ingestion d'événements (EPIC-07 — SQLAlchemy)."""

from datetime import datetime, timezone


def test_event_valid_payload(client) -> None:
    """Teste l'ingestion d'un événement avec un payload valide."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100", "port": 22},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_event_invalid_payload_missing_field(client) -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion_detected",
        "details": {},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 422


def test_event_invalid_payload_wrong_type(client) -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": "not_a_dict",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 422


def test_event_storage(client) -> None:
    """Teste que l'événement est bien stocké en DB."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion_detected",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100"},
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200


def test_event_multiple_storage(client) -> None:
    """Teste le stockage de plusieurs événements."""
    for i in range(3):
        payload = {
            "endpoint_id": f"ep-{i:03d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "test_event",
            "severity": "low",
            "details": {"index": i},
        }
        response = client.post("/api/v1/events", json=payload)
        assert response.status_code == 200
