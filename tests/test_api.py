from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Basketball Team" in data


def test_signup_and_remove_participant():
    activity = "Basketball Team"
    email = "test.user@example.com"

    # Ensure email is not already signed up
    response = client.get(f"/activities")
    assert response.status_code == 200
    before = response.json()
    assert email not in before[activity]["participants"]

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify participant appears
    response = client.get(f"/activities")
    assert response.status_code == 200
    after = response.json()
    assert email in after[activity]["participants"]

    # Remove participant
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    # Verify removed
    response = client.get(f"/activities")
    assert response.status_code == 200
    final = response.json()
    assert email not in final[activity]["participants"]


def test_remove_nonexistent_participant():
    activity = "Basketball Team"
    email = "noone@example.com"

    # Ensure this email is not on the list
    response = client.get(f"/activities")
    assert response.status_code == 200
    data = response.json()
    if email in data[activity]["participants"]:
        # if it exists (unlikely), remove it first
        client.delete(f"/activities/{activity}/participants?email={email}")

    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 404
