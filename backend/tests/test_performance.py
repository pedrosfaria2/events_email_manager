import time

def test_create_event_performance(client):
    start_time = time.time()

    for i in range(1000):
        response = client.post('/events', json={
            'title': f'Test Event {i}',
            'description': 'This is a test event',
            'date': '2024-12-31',
            'startTime': '10:00',
            'endTime': '11:00',
            'tags': 'performance'
        })
        assert response.status_code == 201

    elapsed_time = time.time() - start_time
    print(f"Time to create 100 events: {elapsed_time:.2f} seconds")
    assert elapsed_time < 10  # Verifica se a criação de 100 eventos leva menos de 10 segundos

def test_get_events_performance(client):
    start_time = time.time()

    response = client.get('/events')
    assert response.status_code == 200

    elapsed_time = time.time() - start_time
    print(f"Time to fetch events: {elapsed_time:.2f} seconds")
    assert elapsed_time < 1  # Verifica se a recuperação dos eventos leva menos de 2 segundos
