from fastapi.testclient import TestClient
from main import app
import config

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_missing_webhook_secret():
    payload = {
        "market_id": "0x123",
        "token_id": "0x456",
        "side": "BUY",
        "confidence": 95.0,
        "news_source": "Test Headline"
    }
    response = client.post("/api/v1/trade", json=payload)
    # Should fail due to missing x-webhook-secret header
    assert response.status_code == 422 

def test_invalid_webhook_secret():
    payload = {
        "market_id": "0x123",
        "token_id": "0x456",
        "side": "BUY",
        "confidence": 95.0,
        "news_source": "Test Headline"
    }
    headers = {"x-webhook-secret": "wrong-secret"}
    response = client.post("/api/v1/trade", json=payload, headers=headers)
    assert response.status_code == 401

def test_valid_trade_payload():
    config.MIN_CONFIDENCE_THRESHOLD = 80.0  # Override for test
    payload = {
        "market_id": "0x123",
        "token_id": "0x456",
        "side": "BUY",
        "confidence": 90.0, # High confidence
        "news_source": "Test Headline"
    }
    headers = {"x-webhook-secret": config.WEBHOOK_SECRET}
    response = client.post("/api/v1/trade", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_low_confidence_rejection():
    config.MIN_CONFIDENCE_THRESHOLD = 90.0
    payload = {
        "market_id": "0x123",
        "token_id": "0x456",
        "side": "BUY",
        "confidence": 85.0, # Fails threshold
        "news_source": "Test Headline"
    }
    headers = {"x-webhook-secret": config.WEBHOOK_SECRET}
    response = client.post("/api/v1/trade", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Confidence below threshold" in data["error_message"]
