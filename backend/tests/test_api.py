import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "components" in data

def test_citizens_endpoint():
    response = client.get("/api/v1/welfare/citizens")
    assert response.status_code == 200
    assert "citizens" in response.json()

def test_logs_endpoint():
    response = client.get("/api/v1/welfare/logs")
    assert response.status_code == 200
    assert "logs" in response.json()

def test_notifications_endpoint():
    response = client.get("/api/v1/welfare/notifications")
    assert response.status_code == 200
    assert "notifications" in response.json()

def test_recommend_schemes_endpoint():
    payload = {
        "full_name": "Test Citizen",
        "dob": "1990-01-01",
        "income_annual": 200000.0,
        "state": "Tamil Nadu",
        "document_type": "Income Certificate"
    }
    response = client.post("/api/v1/welfare/recommend-schemes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "extracted_data" in data
    assert "eligibility" in data
    assert "recommendations" in data
    assert "explanation" in data
