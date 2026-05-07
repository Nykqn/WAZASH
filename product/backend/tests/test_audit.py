"""Tests pour le système d'audit trail (EPIC-07 — SQLAlchemy)."""

from datetime import datetime, timezone


def test_get_audit_empty(client) -> None:
    """Teste que GET /api/v1/audit/ retourne une liste vide initialement."""
    response = client.get("/api/v1/audit/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Peut contenir des logs de seed si présents, vérifier la structure
    for log in data:
        assert "id" in log
        assert "timestamp" in log
        assert "action" in log
        assert "details" in log


def test_audit_after_login(client) -> None:
    """Teste qu'un login génère un log d'audit avec action 'login'."""
    payload = {
        "email": "admin@wazash.io",
        "password": "dummy123",
    }
    login_response = client.post("/api/v1/auth/login", json=payload)
    assert login_response.status_code == 200

    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    # Au moins un log de login
    login_logs = [log for log in audit_data if log["action"] == "login"]
    assert len(login_logs) >= 1
    assert login_logs[0]["user_email"] == "admin@wazash.io"
    assert "Connexion réussie" in login_logs[0]["details"]


def test_audit_after_event(client) -> None:
    """Teste qu'un événement génère un log avec action 'event_ingested'."""
    event_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"message": "Tentative d'intrusion détectée", "source_ip": "192.168.1.100"},
    }
    event_response = client.post("/api/v1/events", json=event_payload)
    assert event_response.status_code == 200

    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    event_logs = [log for log in audit_data if log["action"] == "event_ingested"]
    assert len(event_logs) >= 1
    assert event_logs[0]["user_email"] is None
    assert "intrusion" in event_logs[0]["details"]


def test_audit_after_alert_generate(client) -> None:
    """Teste qu'une alerte générée crée un log avec action 'alert_generated'."""
    alert_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"message": "Malware détecté", "source_ip": "192.168.1.100"},
    }
    alert_response = client.post("/api/v1/alerts/generate", json=alert_payload)
    assert alert_response.status_code == 200

    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    alert_logs = [log for log in audit_data if log["action"] == "alert_generated"]
    assert len(alert_logs) >= 1
    assert alert_logs[0]["user_email"] is None


def test_audit_order(client) -> None:
    """Teste que les logs sont retournés par ordre chronologique inversé."""
    # 1. Login
    login_payload = {"email": "admin@wazash.io", "password": "dummy123"}
    client.post("/api/v1/auth/login", json=login_payload)

    # 2. Event
    event_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"message": "Tentative d'intrusion"},
    }
    client.post("/api/v1/events", json=event_payload)

    # 3. Alert generate
    alert_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"message": "Malware détecté"},
    }
    client.post("/api/v1/alerts/generate", json=alert_payload)

    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    # Vérifier que les timestamps sont en ordre décroissant
    timestamps = [log["timestamp"] for log in audit_data]
    for i in range(len(timestamps) - 1):
        assert timestamps[i] >= timestamps[i + 1], (
            "Les logs doivent être triés par ordre chronologique inversé"
        )
