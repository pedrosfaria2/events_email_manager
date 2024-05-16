def test_add_event(client):
    response = client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Event added successfully'

def test_get_events(client):
    client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31'
    })
    response = client.get('/events')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Event'

def test_add_notification(client):
    response = client.post('/notifications', json={
        'subject': 'Test Notification',
        'message': 'This is a test notification'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Notification added successfully'

def test_get_notifications(client):
    client.post('/notifications', json={
        'subject': 'Test Notification',
        'message': 'This is a test notification'
    })
    response = client.get('/notifications')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['subject'] == 'Test Notification'
