import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "participants" in activity
        assert "max_participants" in activity

def test_signup_and_duplicate():
    # Use a unique email for test
    email = "pytestuser@mergington.edu"
    activity = list(client.get("/activities").json().keys())[0]
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister():
    email = "pytestuser2@mergington.edu"
    activity = list(client.get("/activities").json().keys())[0]
    # Sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
