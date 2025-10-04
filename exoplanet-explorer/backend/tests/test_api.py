"""
Basic unit tests for the API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_missions():
    """Test missions endpoint"""
    response = client.get("/api/v1/missions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_search_planets():
    """Test planets search endpoint"""
    response = client.get("/api/v1/planets?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "planets" in data
    assert "total" in data
    assert isinstance(data["planets"], list)


def test_search_stars():
    """Test stars search endpoint"""
    response = client.get("/api/v1/stars/search?query=TOI-100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_ml_models():
    """Test ML models endpoint"""
    response = client.get("/api/v1/ml/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert isinstance(data["models"], list)


def test_ml_classify():
    """Test ML classification endpoint"""
    features = {
        "period": 3.14,
        "radius": 1.2,
        "mass": 1.1
    }
    response = client.post("/api/v1/ml/classify", json={
        "features": features,
        "model_type": "random_forest"
    })
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "probabilities" in data