"""Tests pour l'authentification."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_valid() -> None:
    """Teste la connexion avec des identifiants valides."""
    payload = {
        "email": "admin@wazash.io",
        "password": "dummy123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_invalid() -> None:
    """Teste la connexion avec des identifiants invalides."""
    payload = {
        "email": "admin@wazash.io",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


def test_login_invalid_payload_missing_field() -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    # Sans email
    payload = {"password": "dummy123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422

    # Sans password
    payload = {"email": "admin@wazash.io"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422


def test_login_invalid_payload_wrong_type() -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "email": 123,  # devrait être une string
        "password": "dummy123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422
