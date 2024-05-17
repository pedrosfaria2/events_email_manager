import pytest

def test_create_event_with_invalid_data(client):
    # Tentar criar um evento sem título
    response = client.post('/events', json={
        'description': 'This event has no title',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'invalid'
    })
    assert response.status_code == 400  # Bad Request

    # Tentar criar um evento sem data
    response = client.post('/events', json={
        'title': 'Invalid Event',
        'description': 'This event has no date',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'invalid'
    })
    assert response.status_code == 400  # Bad Request
