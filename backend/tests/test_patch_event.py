def test_patch_event(client):
    # Criar um evento antes de tentar atualizar parcialmente
    response = client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'meeting, client'
    })
    assert response.status_code == 201

    # Obter o evento criado
    response = client.get('/events')
    data = response.get_json()
    assert data is not None
    assert len(data) > 0  # Certificar que há eventos
    event_id = data[0]['id']

    # Atualizar parcialmente o evento
    response = client.patch(f'/events/{event_id}', json={
        'description': 'Updated description'
    })
    assert response.status_code == 200

    # Verificar se o evento foi atualizado parcialmente
    response = client.get(f'/events/{event_id}')
    data = response.get_json()
    assert data['description'] == 'Updated description'
