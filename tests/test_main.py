from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200


def test_slack_event_verification():
    event_data = {
        "token": "token",
        "challenge": "test_challenge",
        "type": "url_verification",
    }
    response = client.post(
        "/slack/event_verification", json=event_data
    )
    assert response.status_code == 200
    assert response.json() == {"challenge": "test_challenge"}
