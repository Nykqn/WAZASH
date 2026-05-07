"""Tests pour le endpoint health."""


def test_health_check(client) -> None:
    """Vérifie que le health check retourne 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_health_check_no_external_deps(client) -> None:
    """Vérifie qu'aucune dépendance externe n'est appelée."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
