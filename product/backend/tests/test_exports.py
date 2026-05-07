"""Tests pour les exports CSV (EPIC-09)."""

from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_heartbeats_json() -> None:
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "up",
    }
    client.post("/api/v1/heartbeat", json=payload)
    response = client.get("/api/v1/heartbeats")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert len(data) >= 1


def test_get_heartbeats_csv() -> None:
    response = client.get("/api/v1/heartbeats", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "endpoint_id" in response.text


def test_get_heartbeats_filter_status() -> None:
    payload = {
        "endpoint_id": "ep-002",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "down",
    }
    client.post("/api/v1/heartbeat", json=payload)
    response = client.get("/api/v1/heartbeats", params={"status": "down"})
    assert response.status_code == 200
    data = response.json()
    assert all(hb["status"] == "down" for hb in data)


def test_get_events_json() -> None:
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"source_ip": "10.0.0.1"},
    }
    client.post("/api/v1/events", json=payload)
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_events_csv() -> None:
    response = client.get("/api/v1/events", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "event_type" in response.text


def test_get_events_filter_severity() -> None:
    response = client.get("/api/v1/events", params={"severity": "high"})
    assert response.status_code == 200
    data = response.json()
    assert all(e["severity"] == "high" for e in data)


def test_get_alerts_csv() -> None:
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {},
    }
    client.post("/api/v1/events", json=payload)
    response = client.get("/api/v1/alerts/", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "rule_name" in response.text


def test_get_alerts_filter_status() -> None:
    response = client.get("/api/v1/alerts/", params={"status": "open"})
    assert response.status_code == 200
    data = response.json()
    assert all(a["status"] == "open" for a in data)


def test_get_audit_csv() -> None:
    response = client.get("/api/v1/audit/", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "action" in response.text


def test_get_audit_filter_action() -> None:
    client.post("/api/v1/auth/login", json={"email": "admin@wazash.io", "password": "dummy123"})
    response = client.get("/api/v1/audit/", params={"action": "login"})
    assert response.status_code == 200
    data = response.json()
    assert all(log["action"] == "login" for log in data)
