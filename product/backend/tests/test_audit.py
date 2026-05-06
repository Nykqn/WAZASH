"""Tests pour le système d'audit trail (EPIC-05)."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.core import storage

client = TestClient(app)


def setup_function() -> None:
    """Vide les stockages avant chaque test."""
    storage.heartbeats_store.clear()
    storage.events_store.clear()
    storage.alerts_store.clear()
    storage.audit_store.clear()
    storage.audit_id_counter = 0
    storage.alert_id_counter = 0


def test_get_audit_empty() -> None:
    """Teste que GET /api/v1/audit/ retourne une liste vide initialement."""
    response = client.get("/api/v1/audit/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_audit_after_login() -> None:
    """Teste qu'un login génère un log d'audit avec action 'login'."""
    # Vider les logs d'audit
    storage.audit_store.clear()

    # Effectuer un login valide
    payload = {
        "email": "admin@wazash.io",
        "password": "dummy123",
    }
    login_response = client.post("/api/v1/auth/login", json=payload)
    assert login_response.status_code == 200

    # Vérifier les logs d'audit
    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    assert len(audit_data) == 1
    assert audit_data[0]["action"] == "login"
    assert audit_data[0]["user_email"] == "admin@wazash.io"
    assert "Connexion réussie" in audit_data[0]["details"]
    assert "id" in audit_data[0]
    assert "timestamp" in audit_data[0]


def test_audit_after_event() -> None:
    """Teste qu'un événement génère un log avec action 'event_ingested'."""
    # Vider les logs d'audit
    storage.audit_store.clear()

    # Envoyer un événement (format EventPayload)
    event_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"message": "Tentative d'intrusion détectée", "source_ip": "192.168.1.100"},
    }
    event_response = client.post("/api/v1/events", json=event_payload)
    assert event_response.status_code == 200

    # Vérifier les logs d'audit
    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    # Il doit y avoir au moins un log (event_ingested)
    # Si le event déclenche aussi une alerte, il y en aura plus
    event_logs = [log for log in audit_data if log["action"] == "event_ingested"]
    assert len(event_logs) >= 1

    event_log = event_logs[0]
    assert event_log["action"] == "event_ingested"
    assert event_log["user_email"] is None
    assert "intrusion" in event_log["details"]
    assert "ingéré" in event_log["details"]


def test_audit_after_alert_generate() -> None:
    """Teste qu'une alerte générée crée un log avec action 'alert_generated'."""
    # Vider les logs d'audit
    storage.audit_store.clear()

    # Générer une alerte (format EventPayload)
    alert_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"message": "Malware détecté", "source_ip": "192.168.1.100"},
    }
    alert_response = client.post("/api/v1/alerts/generate", json=alert_payload)
    assert alert_response.status_code == 200

    # Vérifier les logs d'audit
    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    # Vérifions qu'il y a au moins un log avec action "alert_generated"
    alert_logs = [log for log in audit_data if log["action"] == "alert_generated"]
    assert len(alert_logs) >= 1

    alert_log = alert_logs[0]
    assert alert_log["action"] == "alert_generated"
    assert alert_log["user_email"] is None
    assert "malware" in alert_log["details"].lower() or "alerte" in alert_log["details"].lower()


def test_audit_order() -> None:
    """Teste que les logs sont retournés par ordre chronologique inversé."""
    # Vider les logs d'audit
    storage.audit_store.clear()

    # Effectuer plusieurs actions dans l'ordre
    # 1. Login
    login_payload = {
        "email": "admin@wazash.io",
        "password": "dummy123",
    }
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200

    # 2. Envoyer un événement
    event_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "intrusion",
        "severity": "high",
        "details": {"message": "Tentative d'intrusion", "source_ip": "192.168.1.100"},
    }
    event_response = client.post("/api/v1/events", json=event_payload)
    assert event_response.status_code == 200

    # 3. Générer une alerte
    alert_payload = {
        "endpoint_id": "endpoint-001",
        "timestamp": datetime.now().isoformat(),
        "event_type": "malware",
        "severity": "critical",
        "details": {"message": "Malware détecté", "source_ip": "192.168.1.100"},
    }
    alert_response = client.post("/api/v1/alerts/generate", json=alert_payload)
    assert alert_response.status_code == 200

    # Vérifier l'ordre des logs (plus récent d'abord)
    audit_response = client.get("/api/v1/audit/")
    assert audit_response.status_code == 200
    audit_data = audit_response.json()

    # Il doit y avoir au moins 3 logs (login, event_ingested, alert_generated)
    # (event peut générer aussi une alerte, donc il peut y en avoir plus)
    assert len(audit_data) >= 3

    # Vérifier que les timestamps sont en ordre décroissant
    timestamps = [log["timestamp"] for log in audit_data]
    for i in range(len(timestamps) - 1):
        assert timestamps[i] >= timestamps[i + 1], (
            "Les logs doivent être triés par ordre chronologique inversé"
        )

    # Le premier log doit être l'alerte générée (dernière action)
    # ou une action liée à la génération d'alerte
    actions = [log["action"] for log in audit_data]
    # La dernière action effectuée était alert_generate, donc "alert_generated" devrait être en premier
    assert "alert_generated" in actions
