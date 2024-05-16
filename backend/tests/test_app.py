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

def test_update_event(client):
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
    data = response.get_json()
    event_id = data[0]['id']

    response = client.put(f'/events/{event_id}', json={
        'title': 'Updated Test Event',
        'description': 'This is an updated test event',
        'date': '2024-12-31',
        'startTime': '11:00',
        'endTime': '12:00',
        'recurrence': 2,
        'allDay': True
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Event updated successfully'

    response = client.get('/events')
    data = response.get_json()
    event = data[0]
    assert event['title'] == 'Updated Test Event'
    assert event['description'] == 'This is an updated test event'
    assert event['date'].startswith('2024-12-31')


def test_delete_event(client):
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
    data = response.get_json()
    event_id = data[0]['id']

    response = client.delete(f'/events/{event_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Event deleted successfully'

    response = client.get('/events')
    data = response.get_json()
    assert len(data) == 0

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
