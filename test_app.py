import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_events_endpoint_with_valid_date_range(client):
    # Define a valid date range
    valid_date_range = {
        "league": "NFL",
        "startDate": "2023-01-01",
        "endDate": "2023-01-31"
    }
    # Send POST request to /events endpoint
    response = client.post('/events', json=valid_date_range)
    # Check status code
    assert response.status_code == 200
    # Check response content
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0
    for event in data:
        assert event['eventDate'] >= valid_date_range['startDate']
        assert event['eventDate'] <= valid_date_range['endDate']


def test_events_endpoint_with_invalid_date_range(client):
    # Define an invalid date range (end date before start date)
    invalid_date_range = {
        "league": "NFL",
        "startDate": "2023-01-31",
        "endDate": "2023-01-01"
    }
    # Send POST request to /events endpoint
    response = client.post('/events', json=invalid_date_range)
    # Check status code
    assert response.status_code == 400
    # Check response content
    data = response.json
    assert 'error' in data


def test_events_endpoint_with_different_leagues(client):
    # Define a request with a different league (e.g., NBA)
    nba_request = {
        "league": "NBA",
        "startDate": "2023-01-01",
        "endDate": "2023-01-31"
    }
    # Send POST request to /events endpoint with NBA league
    response = client.post('/events', json=nba_request)
    # Check status code
    assert response.status_code == 200
    # Check response content
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0
    for event in data:
        assert event['eventDate'] >= nba_request['startDate']
        assert event['eventDate'] <= nba_request['endDate']