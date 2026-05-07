"""Tests pour le système de corrélation IP (EPIC-05)."""

from datetime import datetime, timezone


def test_correlation_empty(client) -> None:
    """Teste que GET /api/v1/correlations retourne une liste vide."""
    resp = client.get("/api/v1/correlations")
    assert resp.status_code == 200
    assert resp.json() == []


def test_correlation_after_two_events(client) -> None:
    """Teste que 2 événements même IP ne créent pas encore une corrélation."""
    for _ in range(2):
        payload = {
            "endpoint_id": "ep-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "scan",
            "severity": "medium",
            "details": {"source_ip": "10.0.0.99", "target_port": 22},
        }
        client.post("/api/v1/events", json=payload)

    resp = client.get("/api/v1/correlations")
    assert resp.status_code == 200
    assert resp.json() == []


def test_correlation_after_three_events(client) -> None:
    """Teste que 3 événements même IP créent une corrélation."""
    for i in range(3):
        payload = {
            "endpoint_id": "ep-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "scan",
            "severity": "medium",
            "details": {"source_ip": "10.0.0.99", "target_port": 22 + i},
        }
        client.post("/api/v1/events", json=payload)

    resp = client.get("/api/v1/correlations")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    corr = data[0]
    assert corr["correlation_type"] == "ip_repetition"
    assert corr["source_ip"] == "10.0.0.99"
    assert corr["event_count"] >= 3


def test_correlation_multiple_ips(client) -> None:
    """Teste que différentes IP créent des corrélations séparées."""
    for ip in ["10.0.0.10", "10.0.0.11"]:
        for _ in range(3):
            payload = {
                "endpoint_id": "ep-001",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "scan",
                "severity": "medium",
                "details": {"source_ip": ip, "target_port": 22},
            }
            client.post("/api/v1/events", json=payload)

    resp = client.get("/api/v1/correlations")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    ips = {c["source_ip"] for c in data}
    assert "10.0.0.10" in ips
    assert "10.0.0.11" in ips


def test_correlation_without_source_ip(client) -> None:
    """Teste qu'un événement sans source_ip ne crée pas de corrélation."""
    for _ in range(3):
        payload = {
            "endpoint_id": "ep-001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "info",
            "severity": "low",
            "details": {"message": "test sans IP"},
        }
        client.post("/api/v1/events", json=payload)

    resp = client.get("/api/v1/correlations")
    assert resp.status_code == 200
    assert resp.json() == []
