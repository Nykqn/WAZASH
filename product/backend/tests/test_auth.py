"""Tests pour l'authentification (EPIC-07 — JWT + bcrypt)."""


def test_login_valid(client) -> None:
    """Teste la connexion avec des identifiants valides."""
    payload = {
        "email": "admin@wazash.io",
        "password": "dummy123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] != "dummy-token-123"  # Doit être un vrai JWT
    assert data["token_type"] == "bearer"


def test_login_invalid(client) -> None:
    """Teste la connexion avec des identifiants invalides."""
    payload = {
        "email": "admin@wazash.io",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


def test_login_invalid_payload_missing_field(client) -> None:
    """Teste le rejet d'un payload incomplet (champ manquant)."""
    payload = {"password": "dummy123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422

    payload = {"email": "admin@wazash.io"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422


def test_login_invalid_payload_wrong_type(client) -> None:
    """Teste le rejet d'un payload avec un mauvais type."""
    payload = {
        "email": 123,
        "password": "dummy123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422


def test_login_unknown_user(client) -> None:
    """Teste la connexion avec un utilisateur inexistant."""
    payload = {
        "email": "unknown@wazash.io",
        "password": "dummy123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


def test_login_user_analyst(client) -> None:
    """Teste la connexion avec l'utilisateur analyste."""
    payload = {
        "email": "user@wazash.io",
        "password": "test456",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
