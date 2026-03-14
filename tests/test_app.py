import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act - signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Act - unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert unregister_resp.status_code == 200
    assert f"Removed {email}" in unregister_resp.json()["message"]

    # Clean up: try to unregister again, should fail
    unregister_again = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_again.status_code == 404
    assert "Participant not found" in unregister_again.json()["detail"]
