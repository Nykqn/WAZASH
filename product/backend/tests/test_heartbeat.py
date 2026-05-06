"""Tests pour l'ingestion de heartbeats."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.core.storage import get_heartbeats, heartbeats_store
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    """Vide le stockage avant chaque test."""
    heartbeats_store.clear()


def test_heartbeat_valid_payload() -> None:
    """Teste l'ingestion d'un heartbeat avec un payload valide."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_heartbeat_invalid_payload_missing_field() -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    payload = {
        "endpoint_id": "ep-001",
        # timestamp manquant
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 422


def test_heartbeat_invalid_payload_wrong_type() -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "endpoint_id": 123,  # devrait être une string
        "timestamp": datetime.now().isoformat(),
        "status": "up",
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 422


def test_heartbeat_storage() -> None:
    """Teste que le heartbeat est bien stocké en mémoire."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now().isoformat(),
        "status": "up",
    }
    client.post("/api/v1/heartbeat", json=payload)

    heartbeats = get_heartbeats()
    assert len(heartbeats) == 1
    assert heartbeats[0]["endpoint_id"] == "ep-001"
    assert heartbeats[0]["status"] == "up"


def test_heartbeat_multiple_storage() -> None:
    """Teste le stockage de plusieurs heartbeats."""
    for i in range(3):
        payload = {
            "endpoint_id": f"ep-{i:03d}",
            "timestamp": datetime.now().isoformat(),
            "status": "up",
        }
        client.post("/api/v1/heartbeat", json=payload)

    heartbeats = get_heartbeats()
    assert len(heartbeats) == 3
