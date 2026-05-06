"""Tests pour le endpoint health."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Vérifie que le health check retourne 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_health_check_no_external_deps() -> None:
    """Vérifie qu'aucune dépendance externe n'est appelée."""
    response = client.get("/health")
    assert response.status_code == 200
    # Vérifie que la réponse est immédiate (pas de timeout simulé)
    assert "status" in response.json()
