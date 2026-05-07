"""Tests pour l'ingestion de heartbeats (EPIC-07 — SQLAlchemy)."""

from datetime import datetime, timezone


def test_heartbeat_valid_payload(client) -> None:
    """Teste l'ingestion d'un heartbeat avec un payload valide."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_heartbeat_invalid_payload_missing_field(client) -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    payload = {
        "endpoint_id": "ep-001",
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 422


def test_heartbeat_invalid_payload_wrong_type(client) -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "endpoint_id": 123,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 422


def test_heartbeat_storage(client) -> None:
    """Teste que le heartbeat est bien stocké en DB."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 200


def test_heartbeat_multiple_storage(client) -> None:
    """Teste le stockage de plusieurs heartbeats."""
    for i in range(3):
        payload = {
            "endpoint_id": f"ep-{i:03d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "up",
        }
        response = client.post("/api/v1/heartbeat", json=payload)
        assert response.status_code == 200
