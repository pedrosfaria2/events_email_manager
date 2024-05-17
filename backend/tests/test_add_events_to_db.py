import pytest
from backend.models import db, Event
from backend.add_event_to_db import add_events_to_db

def test_add_events_to_db(init_db, sample_events):
    add_events_to_db(sample_events)
    
    events = Event.query.all()
    assert len(events) == 2
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"
