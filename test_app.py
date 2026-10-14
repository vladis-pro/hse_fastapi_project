from fastapi.testclient import TestClient

from app_final import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_system():
    response = client.get("/system")

    assert response.status_code == 200
    assert "hostname" in response.json()
    assert "os" in response.json()


def test_memory_gb():
    response = client.get("/memory?unit=gb")

    assert response.status_code == 200
    assert response.json()["unit"] == "gb"


def test_memory_invalid_unit():
    response = client.get("/memory?unit=abc")

    assert response.status_code == 400
    assert response.json()["detail"] == "Unit must be 'gb' or 'mb'"