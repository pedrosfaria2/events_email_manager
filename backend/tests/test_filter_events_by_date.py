from backend.models import Event, Notification, db
from datetime import date

def test_filter_events_by_date(client, init_db):
    # Adicionar eventos de teste
    event1 = Event(title="Evento 1", description="Descrição 1", date=date(2024, 5, 17), start_time="08:00", end_time="19:00", tags="tag1")
    event2 = Event(title="Evento 2", description="Descrição 2", date=date(2024, 6, 18), start_time="09:00", end_time="17:00", tags="tag2")
    db.session.add_all([event1, event2])
    db.session.commit()

    # Filtrar eventos entre 2024-05-01 e 2024-05-31
    response = client.get('/events?start=2024-05-01&end=2024-05-31')
    assert response.status_code == 200
    events = response.get_json()
    assert len(events) == 1
    assert events[0]['title'] == "Evento 1"

    # Filtrar eventos entre 2024-06-01 e 2024-06-30
    response = client.get('/events?start=2024-06-01&end=2024-06-30')
    assert response.status_code == 200
    events = response.get_json()
    assert len(events) == 1
    assert events[0]['title'] == "Evento 2"
