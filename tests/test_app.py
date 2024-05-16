def test_add_event(client):
    response = client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'recurrence': 1,
        'allDay': False
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Event added successfully'

def test_get_events(client):
    client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'recurrence': 1,
        'allDay': False
    })
    response = client.get('/events')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    event = data[0]
    assert event['title'] == 'Test Event'
    assert event['description'] == 'This is a test event'
    assert event['date'] == '2024-12-31'
    assert event['start_time'] == '10:00'
    assert event['end_time'] == '11:00'
    assert event['recurrence'] == 1
    assert event['all_day'] == False

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
    notification = data[0]
    assert notification['subject'] == 'Test Notification'
    assert notification['message'] == 'This is a test notification'
