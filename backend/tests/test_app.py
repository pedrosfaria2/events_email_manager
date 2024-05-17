def test_update_event(client):
    # Criar um evento antes de tentar atualizar
    response = client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'meeting, client'
    })
    print('POST /events response status code:', response.status_code)
    print('POST /events response data:', response.get_data(as_text=True))
    assert response.status_code == 201

    # Obter o evento criado
    response = client.get('/events')
    data = response.get_json()
    print('GET /events response data:', data)
    assert data is not None
    assert len(data) > 0  # Certificar que há eventos
    event_id = data[0]['id']

    # Atualizar o evento
    response = client.put(f'/events/{event_id}', json={
        'title': 'Updated Test Event',
        'description': 'This is an updated test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'meeting, client'
    })
    print('PUT /events/<event_id> response status code:', response.status_code)
    print('PUT /events/<event_id> response data:', response.get_data(as_text=True))
    assert response.status_code == 200

    # Verificar se o evento foi atualizado
    response = client.get(f'/events/{event_id}')  # Certifique-se de que essa rota existe
    data = response.get_json()
    print('GET /events/<event_id> response data:', data)
    assert data['title'] == 'Updated Test Event'

def test_delete_event(client):
    # Criar um evento antes de tentar deletar
    response = client.post('/events', json={
        'title': 'Test Event',
        'description': 'This is a test event',
        'date': '2024-12-31',
        'startTime': '10:00',
        'endTime': '11:00',
        'tags': 'meeting, client'
    })
    print('POST /events response status code:', response.status_code)
    print('POST /events response data:', response.get_data(as_text=True))
    assert response.status_code == 201

    # Obter o evento criado
    response = client.get('/events')
    data = response.get_json()
    print('GET /events response data:', data)
    assert data is not None
    assert len(data) > 0  # Certificar que há eventos
    event_id = data[0]['id']

    # Deletar o evento
    response = client.delete(f'/events/{event_id}')
    print('DELETE /events/<event_id> response status code:', response.status_code)
    print('DELETE /events/<event_id> response data:', response.get_data(as_text=True))
    assert response.status_code == 200

    # Verificar se o evento foi deletado
    response = client.get(f'/events/{event_id}')
    print('GET /events/<event_id> response status code:', response.status_code)
    print('GET /events/<event_id> response data:', response.get_data(as_text=True))
    assert response.status_code == 404  # Atualizado para refletir a verificação correta
