"""Tests pour le système d'alerte simple (EPIC-07 — SQLAlchemy)."""

from datetime import datetime, timezone


def test_get_alerts_empty(client) -> None:
    """Teste que GET /api/v1/alerts/ retourne une liste vide initialement."""
    response = client.get("/api/v1/alerts/")
    assert response.status_code == 200
    assert response.json() == []


def test_alert_generation_after_event(client) -> None:
    """Teste qu'un événement de type 'intrusion' génère une alerte."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100", "port": 22},
    }

    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    alerts_response = client.get("/api/v1/alerts/")
    assert alerts_response.status_code == 200

    alerts = alerts_response.json()
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "intrusion_detected"
    assert alerts[0]["severity"] == "critical"
    assert alerts[0]["status"] == "open"
    assert "id" in alerts[0]
    assert "event_id" in alerts[0]
    assert "timestamp" in alerts[0]


def test_alert_no_match(client) -> None:
    """Teste qu'un événement de type non reconnu ne génère pas d'alerte."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "normal",
        "severity": "low",
        "details": {"message": "Rien d'anormal"},
    }

    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    alerts_response = client.get("/api/v1/alerts/")
    assert alerts_response.status_code == 200
    assert alerts_response.json() == []


def test_alert_rule_matching(client) -> None:
    """Teste que la règle 'malware' génère une alerte avec severity 'high'."""
    payload = {
        "endpoint_id": "ep-002",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"file": "/tmp/malware.exe", "signature": "Trojan.Gen.2"},
    }

    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    alerts_response = client.get("/api/v1/alerts/")
    assert alerts_response.status_code == 200

    alerts = alerts_response.json()
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "malware_detected"
    assert alerts[0]["severity"] == "high"
    assert alerts[0]["status"] == "open"


def test_generate_endpoint(client) -> None:
    """Teste POST /api/v1/alerts/generate avec un payload valide."""
    payload = {
        "endpoint_id": "ep-003",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"source_ip": "10.0.0.50", "target_port": 443},
    }

    response = client.post("/api/v1/alerts/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "generated"
    assert "alert_id" in data
    assert data["alert_id"] is not None
    assert "message" in data
    assert "intrusion_detected" in data["message"]


def test_generate_endpoint_no_match(client) -> None:
    """Teste POST /api/v1/alerts/generate avec un type non reconnu."""
    payload = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "unknown_type",
        "severity": "low",
        "details": {"info": "test"},
    }

    response = client.post("/api/v1/alerts/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "no_match"
    assert data["alert_id"] is None
    assert "Aucune règle" in data["message"]


def test_generate_endpoint_invalid_payload(client) -> None:
    """Teste POST /api/v1/alerts/generate avec un payload invalide."""
    payload = {
        "endpoint_id": "ep-001",
        "event_type": "intrusion",
        "severity": "high",
    }

    response = client.post("/api/v1/alerts/generate", json=payload)
    assert response.status_code == 422


def test_multiple_alerts_generation(client) -> None:
    """Teste la génération de plusieurs alertes."""
    payload1 = {
        "endpoint_id": "ep-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"source_ip": "192.168.1.100"},
    }
    response1 = client.post("/api/v1/events", json=payload1)
    assert response1.status_code == 200

    payload2 = {
        "endpoint_id": "ep-002",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"file": "/tmp/virus.exe"},
    }
    response2 = client.post("/api/v1/events", json=payload2)
    assert response2.status_code == 200

    alerts_response = client.get("/api/v1/alerts/")
    assert alerts_response.status_code == 200

    alerts = alerts_response.json()
    assert len(alerts) == 2

    assert alerts[0]["id"] != alerts[1]["id"]

    rule_names = {alert["rule_name"] for alert in alerts}
    assert "intrusion_detected" in rule_names
    assert "malware_detected" in rule_names
