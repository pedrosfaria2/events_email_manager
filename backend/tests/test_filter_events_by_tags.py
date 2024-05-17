def test_filter_events_by_tags(client, init_db):
    # Adicionar eventos de teste
    events = [
        {"title": "Event 1", "description": "Description for Event 1", "date": "2024-05-17", "start_time": "08:00", "end_time": "19:00", "tags": "tag1, tag2"},
        {"title": "Event 2", "description": "Description for Event 2", "date": "2024-05-18", "start_time": "09:00", "end_time": "17:00", "tags": "tag2, tag3"},
        {"title": "Event 3", "description": "Description for Event 3", "date": "2024-05-19", "start_time": "10:00", "end_time": "18:00", "tags": "tag1, tag4"}
    ]
    for event in events:
        client.post('/events', json=event)

    # Filtrar eventos pela tag "tag1"
    response = client.get('/events?tags=tag1')
    assert response.status_code == 200
    data = response.get_json()
    
    # Filtrar eventos pela tag "tag1" e "tag2"
    filtered_data = [event for event in data if "tag1" in event["tags"].split(", ")]

    assert len(filtered_data) == 2
    assert filtered_data[0]['title'] == "Event 1"
    assert filtered_data[1]['title'] == "Event 3"
