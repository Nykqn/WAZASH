"""Tests pour l'inventaire d'actifs (EPIC-08)."""

from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_assets_empty() -> None:
    response = client.get("/api/v1/assets/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_asset() -> None:
    payload = {
        "endpoint_id": "ep-001",
        "hostname": "srv-web-01",
        "ip_address": "192.168.1.10",
        "os": "Ubuntu 22.04",
    }
    response = client.post("/api/v1/assets/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["endpoint_id"] == "ep-001"
    assert data["hostname"] == "srv-web-01"
    assert data["status"] == "active"


def test_create_asset_duplicate() -> None:
    payload = {"endpoint_id": "ep-dup", "hostname": "test"}
    client.post("/api/v1/assets/", json=payload)
    response = client.post("/api/v1/assets/", json=payload)
    assert response.status_code == 409


def test_get_asset() -> None:
    payload = {"endpoint_id": "ep-get", "hostname": "test-get"}
    client.post("/api/v1/assets/", json=payload)
    response = client.get("/api/v1/assets/ep-get")
    assert response.status_code == 200
    assert response.json()["endpoint_id"] == "ep-get"


def test_get_asset_not_found() -> None:
    response = client.get("/api/v1/assets/ep-nonexistent")
    assert response.status_code == 404


def test_update_asset() -> None:
    client.post("/api/v1/assets/", json={"endpoint_id": "ep-patch", "hostname": "old"})
    response = client.patch("/api/v1/assets/ep-patch", json={"hostname": "new", "status": "inactive"})
    assert response.status_code == 200
    data = response.json()
    assert data["hostname"] == "new"
    assert data["status"] == "inactive"


def test_delete_asset() -> None:
    client.post("/api/v1/assets/", json={"endpoint_id": "ep-del"})
    response = client.delete("/api/v1/assets/ep-del")
    assert response.status_code == 204
    response = client.get("/api/v1/assets/ep-del")
    assert response.status_code == 404


def test_list_assets_csv() -> None:
    client.post("/api/v1/assets/", json={"endpoint_id": "ep-csv", "hostname": "csv-test"})
    response = client.get("/api/v1/assets/", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "endpoint_id" in response.text


def test_heartbeat_auto_registers_asset() -> None:
    """Teste qu'un heartbeat d'un endpoint inconnu crée automatiquement l'asset."""
    payload = {
        "endpoint_id": "ep-auto",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "up",
    }
    client.post("/api/v1/heartbeat", json=payload)

    response = client.get("/api/v1/assets/ep-auto")
    assert response.status_code == 200
    data = response.json()
    assert data["endpoint_id"] == "ep-auto"
    assert data["status"] == "up"
