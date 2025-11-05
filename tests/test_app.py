"""
Test suite for the Mergington High School Activities API
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_root():
    """Test the root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect status code
    assert response.headers["location"] == "/static/index.html"  # Check redirect location

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Verify it returns a dictionary
    assert isinstance(activities, dict)
    
    # Check for required fields in each activity
    for activity_name, details in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(details, dict)
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_for_activity_success():
    """Test successful activity signup"""
    test_activity = "Chess Club"
    test_email = "test_student@mergington.edu"
    
    response = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for {test_activity}"

def test_signup_for_nonexistent_activity():
    """Test signing up for a nonexistent activity"""
    response = client.post("/activities/NonexistentClub/signup?email=student@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_duplicate_signup():
    """Test signing up for the same activity twice"""
    test_activity = "Programming Class"
    test_email = "duplicate@mergington.edu"
    
    # First signup
    response = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert response.status_code == 200
    
    # Attempt duplicate signup
    response = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_from_activity_success():
    """Test successful unregistration from activity"""
    test_activity = "Chess Club"
    test_email = "michael@mergington.edu"  # Using an existing participant
    
    response = client.delete(f"/activities/{test_activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {test_email} from {test_activity}"

def test_unregister_from_nonexistent_activity():
    """Test unregistering from a nonexistent activity"""
    response = client.delete("/activities/NonexistentClub/unregister?email=student@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_nonregistered_student():
    """Test unregistering a student who isn't registered"""
    test_activity = "Chess Club"
    test_email = "notregistered@mergington.edu"
    
    response = client.delete(f"/activities/{test_activity}/unregister?email={test_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"