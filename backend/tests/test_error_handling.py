def test_create_event_with_missing_fields(client):
    # Tentar criar um evento sem título e data
    response = client.post('/events', json={
        'description': 'This event has no title and no date',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'invalid'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'title and date are required fields'

def test_update_nonexistent_event(client):
    # Tentar atualizar um evento inexistente
    response = client.put('/events/999', json={
        'title': 'Nonexistent Event',
        'description': 'Trying to update a nonexistent event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'invalid'
    })
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Event not found'

