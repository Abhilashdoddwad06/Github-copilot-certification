import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange: (nothing to arrange for GET)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act: First signup
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: First signup should succeed
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Act: Duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Duplicate signup should fail
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
