from backend.add_event_to_db import add_events_to_db

def test_get_all_events(client, init_db, sample_events):
    # Adicionar eventos de teste
    add_events_to_db(sample_events)
    
    # Obter todos os eventos
    response = client.get('/events')
    assert response.status_code == 200
    events = response.get_json()
    assert len(events) == 2
    assert events[0]['title'] == "Event 1"
    assert events[1]['title'] == "Event 2"
